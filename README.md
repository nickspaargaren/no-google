[![No G](https://raw.githubusercontent.com/nickspaargaren/pihole-google/master/GAFAMSPLATTEXTNOGgit.png)](https://github.com/nickspaargaren/no-google)

# Definition of GAFAM
*The GAFAM is an acronym used to describe the five multinational technology companies Google, Amazon, Facebook, Apple and Microsoft, taking the first letters of all these companies. The GAFAM are sometimes referred to as the Big Five due to them being the five most profilific companies in the world. Although in some sectors some of the five companies may be in direct competition, they offer different products or services overall while presenting some common characteristics that deserve to bring them together under the same acronym: by their size, they are particularly influential on the American and European Internet both economically and politically and socially and are regularly the subject of criticism or prosecution on tax matters, abuses of dominant positions and the non-respect of Internet users' privacy.*

# Purge Google from your network!

Protect yourself from Google's surveillance by using this blocklist! Feel free to criticize our blocklist to make it better and better. Suggestions are welcome!

## How to use it on my Pi-hole?
Simply go into to your blocklist settings to add:
```
https://raw.githubusercontent.com/nickspaargaren/no-google/master/pihole-google.txt
```
Or a selection of the domains :
```
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/shortlinksparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/proxiesparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/productsparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/mailparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/generalparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/fontsparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/firebaseparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/doubleclickparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/domainsparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/dnsparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/androidparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/analyticsparsed
https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/fiberparsed
```

(Combining those with the main whole filter is useless and not recommended, however, feel free to combine the different smaller filters)


## Youtube Advertisements Regex
>^r[0123456789]+((-{3})|(\.))sn-.{8}\.googlevideo\.com$

NOTE: Youtube advertisements are pretty difficult to block trough DNS, as they mainly use a couple of domains for delivering advertisements, but they may also use those same domains for delivering other types of contents that you might not want to block.

## Regex filters
>(.*\.|^)((think)?with)?google($|((adservices|apis|mail|static|syndication|tagmanager|tagservices|usercontent|zip|-analytics)($|\..+)))
>(.*\.|^)g(gpht|mail|static|v(t[12])?)($|\..+)
>(.*\.|^)chrom(e(experiments)?|ium)($|\..+)
>(.*\.|^)ampproject($|\..+)
>(.*\.|^)doubleclick($|\..+)
>(.*\.|^)firebaseio($|\..+)
>(.*\.|^)googlevideo($|\..+)
>(.*\.|^)waze($|\..+)
>(.*\.|^)y(outube|timg)($|\..+)

You can also easily use the modified [pihole regex installer script](https://github.com/mmotti/pihole-regex) by [@mmoti](https://github.com/mmotti) by executing this terminal command from your raspberry Pi Pi-hole server.
```
curl -sSl https://raw.githubusercontent.com/nickspaargaren/no-google/master/install.sh | bash
```
and then, executing it. It should add all of the above regex automatically.


## FAQ

<details>
  <summary>Can I use it with [NextDNS](https://nextdns.io/)?</summary>
  <p>Yep ! It is available in their selection of domains list, labeled as ¨No Google¨. NextDNS is using the wildcard-domains format, so you will have to manually whitelist some specific services, as it will block everything Google related.</p>
</details>

<details>
  <summary>Can I use it with my other ads/domains blocker program ?</summary>
  <p>Surely! If it does indeed support the host or domains type of filters. Import it manually, or [click on this link](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/nickspaargaren/no-google/master/google-domains&title=no-google) if you are using a web browser extension.</p>
</details>

<details>
  <summary>Can I use it with anything other than Pi-hole?</summary>
  <p>Sure thing, the No Google list is declined into multiples formats types, as an host format, domains/urls format and a wildcard format.</p>
</details>

<details>
  <summary>Hum, do you got any mirrors of the list ?</summary>
  <p>Yes indeed, We have a GitLab host mirror of the repo available at this address : https://framagit.org/PoorPocketsMcNewHold/no-google
Note that the main filter is being worked here, so, updates and modifications on the Gitlab source will have to be updated manually.
Otherwise, if you do prefer to use Gitlab, feel free to use it, and even contribute to our list there instead!</p>
</details>

## Can I block the other letters of GAFAM ?
Of course, here’s some filterlists that should help you accomplish that.

**A**pple : https://github.com/c-edw/ios-telemetry, https://github.com/1r2/iosparanoid or https://gitlab.com/CHEF-KOCH/cks-filterlist/blob/master/Anti-Corp/filters/apple.txt

**F**acebook : https://raw.githubusercontent.com/jmdugan/blocklists/master/corporations/facebook/all, https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt or https://gitlab.com/CHEF-KOCH/cks-filterlist/blob/master/Anti-Corp/filters/facebook.txt

**A**mazon : https://github.com/nickspaargaren/no-amazon

**M**icrosoft : https://raw.githubusercontent.com/jmdugan/blocklists/master/corporations/microsoft/all or https://gitlab.com/CHEF-KOCH/cks-filterlist/blob/master/Anti-Corp/filters/microsoft.txt

[![https://gafam.info](https://ptrace.gafam.info/unofficial/img/color/lqdn-gafam-poster-en-color-5x1-2560x.png)](https://gafam.info)
