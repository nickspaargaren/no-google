## Submitting a domain

- Changes will be only be made in the main [pihole-google.txt] source file.
  To submit a new domain, please check if it is not already present.
- The file is divided into sections along different categories, each category is alphabetically sorted.
- When changes are made to the main file, a program is run to automatically update the following files:
  - [AdGuard blocklist]
  - [Pi-hole blocklist]
  - [Unbound blocklist]
  - [per-category blocklist files]

## Suggesting a domain
If you are unable to open a pull request, please open an [issue] and we will investigate.


[issue]: https://github.com/nickspaargaren/no-google/issues/new/choose
[pihole-google.txt]: https://github.com/nickspaargaren/no-google/blob/master/pihole-google.txt
[AdGuard blocklist]: https://github.com/nickspaargaren/no-google/blob/master/pihole-google-adguard.txt
[Pi-hole blocklist]: https://github.com/nickspaargaren/no-google/blob/master/google-domains
[Unbound blocklist]: https://github.com/nickspaargaren/no-google/blob/master/pihole-google-unbound.conf
[per-category blocklist files]: https://github.com/nickspaargaren/no-google/tree/master/categories
