[![No G](https://horobox.co.uk/u/pEP30q.png)](https://github.com/nickspaargaren/pihole-google)

# Definition of GAFAM
*The GAFAM is an acronym used to describe the five multinational technology companies Google, Amazon, Facebook, Apple and Microsoft, taking the first letters of all these companies. The GAFAM are sometimes referred to as the Big Five due to them being the five most profilific companies in the world. Although in some sectors some of the five companies may be in direct competition, they offer different products or services overall while presenting some common characteristics that deserve to bring them together under the same acronym: by their size, they are particularly influential on the American and European Internet both economically and politically and socially and are regularly the subject of criticism or prosecution on tax matters, abuses of dominant positions and the non-respect of Internet users' privacy.*

# Purge Google from your network!

Protect yourself from Google's surveillance by using this blocklist!

Feel free to criticize our blocklist to make it better and better.
Suggestions are completely welcomed!

## Youtube Advertisements Regex
>^r[0123456789]+((-{3})|(\.))sn-.{8}\.googlevideo\.com$

NOTE: This is supposed to prevent these domains to be
loaded not only on youtube, but on all over the web and,
since I'm trying to completely block google in my home,
I don't care if youtube is broken.
I'll may work on an efficient regex for this purpose.

## Regex filters
>^[1234]\.bp\.blogspot\.com

>((.*)\.)?abc\.(.*)

>((.*)\.)?ampproject\.(.*)

>((.*)\.)?android\.(.*)

>((.*)\.)?chrome\.(.*)

>((.*)\.)?chromeexperiments\.(.*)

>((.*)\.)?chromium\.(.*)

>((.*)\.)?doubleclick\.(.*)

>((.*)\.)?firebaseio\.(.*)

>((.*)\.)?ggpht\.(.*)

>((.*)\.)?gmail\.(.*)

>((.*)\.)?google(\.(.*))?

>((.*)\.)?googleadservices\.(.*)

>((.*)\.)?googleapis\.(.*)

>((.*)\.)?googlesyndication\.(.*)

>((.*)\.)?googletagmanager\.(.*)

>((.*)\.)?googletagservices\.(.*)

>((.*)\.)?googleusercontent\.(.*)

>((.*)\.)?google-analytics\.(.*)

>((.*)\.)?gstatic\.(.*)

>((.*)\.)?gv(t[12])?\.(.*)

>((.*)\.)?waze\.(.*)

>((.*)\.)?withgoogle\.(.*)

>((.*)\.)?youtube\.(.*)

>((.*)\.)?ytimg\.(.*)

>.?1e100.

>.?googlebot.

>.?gmodules.

You can also easily use the modified [pihole regex installer script](https://github.com/mmotti/pihole-regex) by [@mmoti](https://github.com/mmotti) by executing this terminal command from your raspberry Pi Pi-hole server.
```
curl -sSl https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/install.sh | bash
```
and then, executing it. It should add all of the above regex automatically.

## Sites you may want to whitelist
>recaptcha.google.com

(Be aware that the regex script doesn´t add it to the whitelist list by default)

## How to use it ?
Simply go into to your blocklist settings to add either, the whole filter `https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/pihole-google.txt
or either a selection of the filtered domains 
```
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/youtubeparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/shortlinksparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/proxiesparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/productsparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/mailparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/generalparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/fontsparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/firebaseparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/doubleclickparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/domainsparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/dnsparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/androidparsed
https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/categories/analyticsparsed
```

(Combining those with the main whole filter is useless and not recommended, however, feel free to combine the different smaller filters)

## Can i use it with my other ads/domains blocker program ?
Surely ! if it does indeed support the host or domains type of filters.
Import it manually, or [click on this link](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/google-domains&title=pihole-google) if you are using a web browser extension.

## Hum, Do you got any mirrors of the list ?
Yes indeed, We have a GitLab host mirror of the repo available at this address : https://framagit.org/PoorPocketsMcNewHold/pihole-google
Note that the main filter is being worked here, so, updates and modifications on the Gitlab source will have to be updated manually.
Otherwise, if you do prefer to use Gitlab, feel free to use it, and even contribute to our list there instead !

## Can i block the other letters of GAFAM ?
Of course, Here´s some filterlist link that have been made by other people.

**A**pple : https://github.com/c-edw/ios-telemetry or https://github.com/1r2/iosparanoid

**F**acebook : https://raw.githubusercontent.com/jmdugan/blocklists/master/corporations/facebook/all or https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt

**A**mazon : Sadly, none to be found. Feel free to let us know of the existence of one !

**M**icrosoft : https://raw.githubusercontent.com/jmdugan/blocklists/master/corporations/microsoft/all

[![https://gafam.info](https://ptrace.gafam.info/unofficial/img/color/lqdn-gafam-poster-en-color-5x1-2560x.png)](https://gafam.info)
