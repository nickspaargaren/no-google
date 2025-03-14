import json
import os
import sqlite3
import subprocess
import logging
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def fetch_url(url):
    """
    Fetches the content of a URL using a GET request.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The content of the URL, or None if an error occurred.
    """
    if not url:
        logging.warning("No URL provided to fetch.")
        return None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
    }

    logging.info(f"Fetching: {url}")

    try:
        response = urlopen(Request(url, headers=headers))
        response_text = response.read().decode("UTF-8").replace("\r\n", "\n")
        # Strip leading/trailing whitespace and remove empty lines
        cleaned_response = "\n".join(line.strip() for line in response_text.splitlines() if line.strip())
        return cleaned_response
    except HTTPError as e:
        logging.error(f"HTTP Error: {e.code} whilst fetching {url}")
    except URLError as e:
        logging.error(f"URL Error: {e.reason} whilst fetching {url}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return None


def get_docker_mount_source(docker_id):
    """
    Retrieves the source mount path for a given Docker container ID, specifically for Pi-hole.

    Args:
        docker_id (str): The ID of the Docker container.

    Returns:
        str: The source mount path if found, otherwise None.
    """
    try:
        docker_mnt = subprocess.check_output(
            ["docker", "inspect", "--format", "{{ (json .Mounts) }}", docker_id],
            text=True  # Use text=True instead of universal_newlines (Python 3.7+)
        ).strip()
        # Convert output to JSON and iterate through each dict
        for json_dict in json.loads(docker_mnt):
            # If this mount's destination is /etc/pihole
            if json_dict["Destination"] == "/etc/pihole":
                # Use the source path as our target
                return json_dict["Source"]
    except subprocess.CalledProcessError as e:
        logging.error(f"Error inspecting Docker container: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from Docker inspect: {e}")
    return None

def run_subprocess_command(command, shell=False):
    """
    Runs a subprocess command and handles common errors.

    Args:
        command (list): The command to run as a list of strings.
        shell (bool, optional): Whether to run the command in a shell. Defaults to False.

    Raises:
        CalledProcessError: If process exits with a non-zero exit code

    Returns:
        str: stdout of the process
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=shell)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {e.cmd}.  Return Code: {e.returncode}.  Error Output: {e.stderr}")
        raise e # Re-raise to stop execution
    except FileNotFoundError:
        logging.error(f"Command not found: {e}")
        raise e # Re-raise to stop execution
    except Exception as e:
        logging.error(f"An unexpected error has occurred: {e}")
        raise e # Re-raise to stop execution


def main():
    url_regexps_remote = "https://raw.githubusercontent.com/nickspaargaren/no-google/master/regex.list"
    install_comment = "github.com/nickspaargaren/no-google"

    cmd_restart = ["pihole", "restartdns", "reload"]

    regexps_remote = set()
    regexps_local = set()
    regexps_mmotti_local = set()  # For DB mode
    regexps_legacy_mmotti = set() # For legacy mode
    regexps_remove = set()

    # Start the docker directory override
    logging.info('Checking for "pihole" docker container')

    # Initialise the docker variables
    docker_id = None
    docker_mnt_src = None

    # Check to see whether the default "pihole" docker container is active
    try:
        docker_id = run_subprocess_command(["docker", "ps", "--filter", "name=pihole", "-q"])
    except FileNotFoundError:
        logging.info("Docker not found. Assuming physical installation.")
    except subprocess.CalledProcessError:
        logging.info("Pihole docker container not found.") # Expected if not running


    # If a pihole docker container was found, locate the first mount
    if docker_id:
        docker_mnt_src = get_docker_mount_source(docker_id)

        # If we successfully found the mount
        if docker_mnt_src:
            logging.info("Running in docker installation mode")
            # Prepend restart commands
            cmd_restart = ["docker", "exec", "-i", "pihole"] + cmd_restart
    else:
        logging.info("Running in physical installation mode ")

    # Set paths
    path_pihole = docker_mnt_src if docker_mnt_src else "/etc/pihole"
    path_legacy_regex = os.path.join(path_pihole, "regex.list")
    path_legacy_mmotti_regex = os.path.join(path_pihole, "mmotti-regex.list")  #Kept for legacy removal
    path_pihole_db = os.path.join(path_pihole, "gravity.db")

    # Check that pi-hole path exists
    if not os.path.exists(path_pihole):
        logging.error(f"{path_pihole} was not found")
        exit(1)

    # Check for write access to /etc/pihole
    if not os.access(path_pihole, os.X_OK | os.W_OK):
        logging.error(f"Write access is not available for {path_pihole}. Please run as root or other privileged user")
        exit(1)
    else:
        logging.info(f"Write access to {path_pihole} verified")

    # Determine whether we are using DB or not
    db_exists = os.path.isfile(path_pihole_db) and os.path.getsize(path_pihole_db) > 0

    if db_exists:
        logging.info("DB detected")
    else:
        logging.info("Legacy regex.list detected")

    # Fetch the remote regexps
    str_regexps_remote = fetch_url(url_regexps_remote)

    # If regexps were fetched, remove any comments and add to set
    if str_regexps_remote:
        regexps_remote.update(
            x for x in str_regexps_remote.splitlines() if x and not x.startswith("#")
        )
        logging.info(f"{len(regexps_remote)} regexps collected from {url_regexps_remote}")
    else:
        logging.error("No remote regexps were found.")
        exit(1)


    if db_exists:
        # DB operations
        try:
            conn = sqlite3.connect(path_pihole_db)
            c = conn.cursor()

            # Add / update remote regexps, using executemany for efficiency and security
            logging.info("Adding / updating regexps in the DB")
            c.executemany(
                "INSERT OR IGNORE INTO domainlist (type, domain, enabled, comment) VALUES (3, ?, 1, ?)",
                [(domain, install_comment) for domain in sorted(regexps_remote)],
            )
            # Update the comments for existing entries.  Important to avoid updating entries that have different comments.
            c.executemany(
                "UPDATE domainlist SET comment = ? WHERE domain = ? AND comment != ?",
                [(install_comment, domain, install_comment) for domain in sorted(regexps_remote)],
            )
            conn.commit()

            # Fetch all current mmotti regexps in the local db
            c.execute(
                "SELECT domain FROM domainlist WHERE type = 3 AND comment = ?",
                (install_comment,),
            )
            regexps_mmotti_local.update(row[0] for row in c.fetchall())

            # Remove any local entries that do not exist in the remote list
            logging.info("Identifying obsolete regexps")
            regexps_remove = regexps_mmotti_local.difference(regexps_remote)

            if regexps_remove:
                logging.info("Removing obsolete regexps")
                c.executemany(
                    "DELETE FROM domainlist WHERE type = 3 AND domain = ?",
                    [(domain,) for domain in regexps_remove],
                )
                conn.commit()

            # Delete mmotti-regex.list as if we've migrated to the db, it's no longer needed
            if os.path.exists(path_legacy_mmotti_regex):
                try:
                    os.remove(path_legacy_mmotti_regex)
                except OSError as e:
                    logging.error(f"Error removing {path_legacy_mmotti_regex}: {e}")


            logging.info("Restarting Pi-hole")
            run_subprocess_command(cmd_restart)


            # Prepare final result
            logging.info("Done - Please see your installed regexps below\n")
            c.execute("SELECT domain FROM domainlist WHERE type = 3")
            final_results = [row[0] for row in c.fetchall()] # List comprehension is faster
            print(*sorted(final_results), sep="\n")

        except sqlite3.Error as e:
            logging.error(f"SQLite error: {e}")
        finally:
            if conn:
                conn.close()

    else:
        # Legacy operations
        # If regex.list exists and is not empty, read it and add to a set
        if os.path.isfile(path_legacy_regex) and os.path.getsize(path_legacy_regex) > 0:
            logging.info("Collecting existing entries from regex.list")
            try:
                with open(path_legacy_regex, "r") as fRead:
                    regexps_local.update(
                        x for x in map(str.strip, fRead) if x and not x.startswith("#")  # Corrected condition
                    )
            except OSError as e:
                logging.error(f"Error reading {path_legacy_regex}: {e}")
                return # Exit if we cannot read existing regex

        # If the local regexp set is not empty
        if regexps_local:
            logging.info(f"{len(regexps_local)} existing regexps identified")
            # If we have a record of a previous legacy install
            if os.path.isfile(path_legacy_mmotti_regex) and os.path.getsize(path_legacy_mmotti_regex) > 0:
                logging.info("Existing mmotti-regex install identified")
                # Read the previously installed regexps to a set
                try:
                    with open(path_legacy_mmotti_regex, "r") as fOpen:
                        regexps_legacy_mmotti.update(
                            x for x in map(str.strip, fOpen) if x and not x.startswith("#")
                        )
                except OSError as e:
                    logging.error(f"Error reading {path_legacy_mmotti_regex}: {e}")
                    # We *can* continue here, as this is not critical

                if regexps_legacy_mmotti:
                    logging.info("Removing previously installed regexps")
                    regexps_local.difference_update(regexps_legacy_mmotti)

        # Add remote regexps to local regexps
        logging.info(f"Syncing with {url_regexps_remote}")
        regexps_local.update(regexps_remote)

        # Output to regex.list
        logging.info(f"Outputting {len(regexps_local)} regexps to {path_legacy_regex}")
        try:
            with open(path_legacy_regex, "w") as fWrite:
                for line in sorted(regexps_local):
                    fWrite.write(f"{line}\n")
        except OSError as e:
            logging.error(f"Error writing to {path_legacy_regex}: {e}")
            return # Exit if we cannot write the regex

        # Output mmotti remote regexps to mmotti-regex.list (for legacy uninstall)
        try:
            with open(path_legacy_mmotti_regex, "w") as fWrite:
                for line in sorted(regexps_remote):
                    fWrite.write(f"{line}\n")
        except OSError as e:
            logging.error(f"Error writing to {path_legacy_mmotti_regex}: {e}")
            # We *can* continue, as this file is only for legacy removal

        logging.info("Restarting Pi-hole")
        run_subprocess_command(cmd_restart)


        # Prepare final result
        logging.info("Done - Please see your installed regexps below\n")
        try:
            with open(path_legacy_regex, "r") as fOpen:
                for line in fOpen:
                    print(line, end="")
        except OSError as e:
            logging.error(f"Error reading {path_legacy_regex}: {e}")
            # We should probably still exit, since we can't show the final list

if __name__ == "__main__":
    main()
