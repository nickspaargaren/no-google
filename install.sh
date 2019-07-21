#!/usr/bin/env bash

#Credits goes of course to mmoti for his regex list script
# Set variables
db_gravity='/etc/pihole/gravity.db'
file_pihole_regex='/etc/pihole/regex.list'
file_mmotti_regex='/etc/pihole/mmotti-regex.list'
file_mmotti_remote_regex='https://github.com/nickspaargaren/pihole-google/blob/master/regex.list'
installer_comment='github.com/nickspaargaren/pihole-google'

# Determine whether we are using Pi-hole DB
if [[ -s "${db_gravity}" ]]; then
	usingDB=true
fi

# Functions
function fetchResults {

	local selection="${1}" action="${2}" queryStr

	# Select * if not set
	[[ -z "${selection}" ]] && selection='*'

	# Determine course of action
	case "${action}" in
		migrated_regexps ) queryStr="Select ${selection} FROM regex WHERE comment='${installer_comment}'";;
		user_created     ) queryStr="Select ${selection} FROM regex WHERE comment IS NULL OR comment!='${installer_comment}'";;
		current_id       ) queryStr="Select ${selection} FROM regex ORDER BY id DESC LIMIT 1";;
		*                ) queryStr="Select ${selection} FROM regex";;
	esac

	# Execute SQL query
	sqlite3 ${db_gravity} "${queryStr}" 2>&1

	# Check exit status
	status="$?"
	[[ "${status}" -ne 0 ]]  && { (>&2 echo '[i] An error occured whilst fetching results'); return 1; }

	return 0
}

function updateDB() {

	local inputData="${1}" action="${2}" queryStr

	# Determine course of action
	case "${action}" in
		remove_pre_migrated ) queryStr="DELETE FROM regex WHERE domain in (${inputData})";;
		remove_migrated     ) queryStr="DELETE FROM regex WHERE comment = '${installer_comment}'";;
		*                   ) return ;;
	esac

	# Execute SQL query
	sudo sqlite3 ${db_gravity} "${queryStr}"

	# Check exit status
	status="$?"
	[[ "${status}" -ne 0 ]]  && { (>&2 echo '[i] An error occured whilst updating database'); return 1; }

	return 0
}

function generateCSV() {

	# Exit if there is a problem with the remoteRegex string
	[[ -z "${1}" ]] && exit 1

	local remoteRegex timestamp queryArr file_csv_tmp

	# Set local variables
	remoteRegex="${1}"
	timestamp="$(date --utc +'%s')"
	file_csv_tmp="$(mktemp -p "/tmp" --suffix=".csv")"
	iteration="$(fetchResults "id" "current_id")"

	# At this point we need to double check that there wasn't an error (rather than no result) when trying to
	# retrieve the current iteration.
	status="$?"
	[[ "${status}" -ne 0 ]] && return 1

	# Create array to hold import string
	declare -a queryArr

	# Start of processing
	# If we got the id of the last item in the regex table, iterate once
	# Otherwise set the iterator to 1
	[[ -n "${iteration}" ]] && ((iteration++)) || iteration=1

	# Iterate through the remote regexps
	# So long as the line is not empty, generate the CSV values
	while read -r regexp; do
		if [[ -n "${regexp}" ]]; then
			queryArr+=("${iteration},\"${regexp}\",1,${timestamp},${timestamp},\"${installer_comment}\"")
			((iteration++))
		fi
	done <<< "${remoteRegex}"

	# If our array is populated then output the results to a temporary file
	if [[ "${#queryArr[@]}" -gt 0 ]]; then
		printf '%s\n' "${queryArr[@]}" > "${file_csv_tmp}"
	else
		return 1
	fi

	# Output the CSV path
	echo "${file_csv_tmp}"

	return 0
}

echo "[i] Fetching mmotti's regexps"
# Fetch the remote regex file and remove comment lines
mmotti_remote_regex=$(wget -qO - "${file_mmotti_remote_regex}" | grep '^[^#]')
# Conditional exit if empty
[[ -z "${mmotti_remote_regex}" ]] && { echo '[i] Failed to download pihole-google regex list'; exit 1; }

echo '[i] Fetching existing regexps'
# Conditionally fetch existing regexps depending on
# whether the user has migrated to the Pi-hole DB or not
if [[ "${usingDB}" == true ]]; then
	str_regex=$(fetchResults "domain")
else
	str_regex=$(grep '^[^#]' < "${file_pihole_regex}")
fi

# Starting the install process
# If we're using the Pi-hole DB
if [[ "${usingDB}" == true ]]; then
	# If we found regexps in the database
	if [[ -n "${str_regex}" ]] ; then
		echo '[i] Checking for previous migration'
		# Check whether this script has previously migrated our regexps
		db_migrated_regexps=$(fetchResults "domain" "migrated_regexps")
		# If migration is detected
		if [[ -n "${db_migrated_regexps}" ]]; then
			echo '[i] Previous migration detected'
			# As we have already migrated the user, we need to check
			# whether the regexps in the database are up-to-date
			echo '[i] Checking whether updates are required'
			# Use comm -3 to suppress lines that appear in both files
			# If there are any results returned, this will quickly tell us
			# that there are discrepancies
			updatesRequired=$(comm -3 <(sort <<< "${db_migrated_regexps}") <(sort <<< "${mmotti_remote_regex}"))
			# Conditional exit if no updates are required
			[[ -z "${updatesRequired}" ]] && { echo '[i] Local regex filter is already up-to-date'; exit 0; }
			# Now we know that updates are required, it's easiest to start a fresh
			echo '[i] Running removal query'
			# Clear our previously migrated domains from the regex table
			updateDB "" "remove_migrated"
		else
			echo '[i] No previous migration detected'
			# As we haven't yet migrated, we need to manually remove matches
			# If we have a local mmotti-regex.list, read from that as it was used on the last install (pre-db)
			# Otherwise, default to the latest remote copy
			if [[ -s "${file_mmotti_regex}" ]]; then
				# Only return regexps in both the regex table and regex file
				mapfile -t result <<< "$(comm -12 <(sort <<< "${str_regex}") <(sort < "${file_mmotti_regex}"))"

			else
				# Only return regexps in both the regex table and regex file
				mapfile -t result <<< "$(comm -12 <(sort <<< "${str_regex}") <(sort <<< "${mmotti_remote_regex}"))"
			fi
			# If we have matches in both the regex table and regex file
			if [[ -n "${result[*]}" ]]; then
				echo '[i] Forming removal string'
				# regexstring --> 'regexstring1','regexstring2',
				# Then remove the trailing comma
				removalStr=$(printf "'%s'," "${result[@]}" | sed 's/,$//')
				# If our removal string is not empty (sanity check)
				if [[ -n "${removalStr}" ]]; then
					echo '[i] Running removal query'
					# Remove regexps from the regex table if there are in the
					# removal string
					updateDB "${removalStr}" "remove_pre_migrated"
				fi
			fi
		fi
	else
		echo '[i] No regexps currently exist in the database'
	fi

	# Create our CSV
	echo '[i] Generating CSV file'
	csv_file=$(generateCSV "${mmotti_remote_regex}")

	# Conditional exit
	if [[ -z "${csv_file}" ]] || [[ ! -s "${csv_file}" ]]; then
		echo '[i] Error: Generated CSV is empty'; exit 1;
	fi

	# Construct correct input format for import
	echo '[i] Importing CSV to DB'
	printf ".mode csv\\n.import \"%s\" %s\\n" "${csv_file}" "regex" | sudo sqlite3 "${db_gravity}" 2>&1

	# Check exit status
	status="$?"
	[[ "${status}" -ne 0 ]]  && { echo '[i] An error occured whilst importing the CSV into the database'; exit 1; }

	# Status update
	echo '[i] Regex import complete'

	# Refresh Pi-hole
	echo '[i] Refreshing Pi-hole'
	pihole restartdns reload > /dev/null

	# Remove the old mmotti-regex file
	[[ -e "${file_mmotti_regex}" ]] && sudo rm -f "${file_mmotti_regex}"

	# Output regexps currently in the DB
	echo $'\n'
	echo 'These are your current regexps:'
	fetchResults "domain" | sed 's/^/  /'
else
	if [[ -n "${str_regex}" ]]; then
		# Restore config prior to previous install
		# Keep entries only unique to pihole regex
		if [[ -s "${file_mmotti_regex}" ]]; then
			echo "[i] Removing pihole-google regex.list from a previous install"
			comm -23 <(sort <<< "${str_regex}") <(sort "${file_mmotti_regex}") | sudo tee $file_pihole_regex > /dev/null
			sudo rm -f "${file_mmotti_regex}"
		else
			# In the event that file_mmotti_regex is not available
			# Match against the latest remote list instead
			echo "[i] Removing pihole-google regex.list from a previous install"
			comm -23 <(sort <<< "${str_regex}") <(sort <<< "${mmotti_remote_regex}") | sudo tee $file_pihole_regex > /dev/null
		fi
	fi

	# Copy latest regex list to file_mmotti_regex dir
	echo "[i] Copying remote regex.list to ${file_mmotti_regex}"
	echo "${mmotti_remote_regex}" | sudo tee "${file_mmotti_regex}" > /dev/null

	# Status update
	echo "[i] $(wc -l <<< "${mmotti_remote_regex}") regexps found in mmotti's regex.list"

	# If pihole regex is not empty after changes
	if [[ -s "${file_pihole_regex}" ]]; then
		# Extract non mmotti-regex entries
		existing_regex_list="$(grep '^[^#]' < "${file_pihole_regex}")"
		# Form output (preserving existing config)
		echo "[i] $(wc -l <<< "$existing_regex_list") regexps exist outside of mmotti's regex.list"
		final_regex=$(printf "%s\n" "${mmotti_remote_regex}" "${existing_regex_list}")
	else
		echo "[i] No regex.list differences to mmotti's regex.list"
		final_regex=$(printf "%s\n" "$mmotti_remote_regex")
	fi

	# Output to regex.list
	echo "[i] Saving to ${file_pihole_regex}"
	LC_COLLATE=C sort -u <<< "${final_regex}" | sudo tee $file_pihole_regex > /dev/null

	# Refresh Pi-hole
	echo "[i] Refreshing Pi-hole"
	pihole restartdns reload > /dev/null

	echo "[i] Done"

	# Output to user
	echo $'\n'
	cat $file_pihole_regex
fi

exit 0
