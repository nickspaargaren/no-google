![No G](https://horobox.co.uk/u/pEP30q.png)
# Purge Google from your network!

Protect yourself from Google's surveillance by using this blocklist!

Feel free to criticize our blocklist to make it better and better.
Suggestions are completely welcomed!


## Youtube Advertisements Regex
>_^r.+\googlevideo.com$_

NOTE: This is supposed to prevent these domains to be
loaded not only on youtube, but on all over the web and,
since I'm trying to completely block google in my home,
I don't care if youtube is broken.
I'll may work on an efficient regex for this purpose.

## Regex filters
>.?android.

>.?chromeexperiments.

>.?doubleclick.

>.?firebaseio.

>.?google.

>.?googleapis.

>.?googlesyndication.

>.?googletagmanager.

>.?googletagservices.

>.?googleusercontent.

>.?gstatic.

>.?google-analytics.

>.?waze.

>.?withgoogle.

>.?youtube.  

## Sites you may want to whitelist
>recaptcha.google.com

## How to use it ?
Simply go into to your blocklist settings to add either, the whole filter `https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/master/pihole-google.txt`
or either a selection of the filtered domains 
```
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/master/categories/youtubeparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/shortlinksparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/proxiesparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/productsparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/mailparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/generalparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/fontsparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/firebaseparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/doubleclickparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/domainsparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/dnsparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/androidparsed
https://raw.githubusercontent.com/PoorPocketsMcNewHold/pihole-google/raw/master/categories/analyticsparsed
```

(Combining those with the main whole filter is useless and not recommended, however, feel free to combine the different smaller filters)

## Can i block the other letters of GAFAM ?
Of course, Here´s some filterlist link that have been made by other people.

**A**pple : Sadly, none to be found. Feel free to let us know of the existance of one !

**F**acebook : https://raw.githubusercontent.com/jmdugan/blocklists/master/corporations/facebook/all or https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt

**A**mazon : Sadly, none to be found. Feel free to let us know of the existance of one !

**M**icrosoft : https://raw.githubusercontent.com/jmdugan/blocklists/master/corporations/microsoft/all

![https://gafam.info](https://ptrace.gafam.info/unofficial/img/color/lqdn-gafam-poster-en-color-5x1-2560x.png)
