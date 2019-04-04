# Purge Google from your network!

Protect yourself from Google's surveillance by using this blocklist!

Feel free to criticize our blocklist to make it better and better.
Suggestions are completely welcomed!

# Regex filters (tested)
>_.?android.
>_.?chromeexperiments.
>_.?doubleclick.
>_.?firebaseio.
>_.?google.
>_.?googleapis.
>_.?googlesyndication.
>_.?googletagmanager.
>_.?googletagservices.
>_.?googleusercontent
>_.?gstatic.
>_.?google-analytics.
>_.?waze.
>_.?withgoogle.
>_.?youtube.

## Youtube Advertisements Regex
>_^r.+\googlevideo.com$_

NOTE: This is supposed to prevent these domains to be
loaded not only on youtube, but on all over the web and,
since I'm trying to completely block google in my home,
I don't care if youtube is broken.
I'll may work on an efficient regex for this purpose.

## **Experimental** regexes
>_^(.+[-_.])??google[-_.]

>_^(.+[-_.])??gstatic[-_.]

>_^(.+[-_.])??googleapis[-_.]

>_^(.+[-_.])??withgoogle[-_.]

>_^(.+[-_.])??googletagmanager[-_.]

>_^(.+[-_.])??googletagservices[-_.]

>_^(.+[-_.])??googleusercontent[-_.]

>_^(.+[-_.])??googlesyndication[-_.]

>_^(.+[-_.])??chromeexperiments[-_.]

>_^(.+[-_.])??google-analytics[-_.]

>_^(.+[-_.])??youtube[-_.]

>_^(.+[-_.])??waze[-_.]

>_^(.+[-_.])??doubleclick[-_.]

>_^(.+[-_.])??firebaseio[-_.]_

These **should** block all domains like this: *.<domain>.*.
They certainly need to be improved, for example idk if they work with domains like this: .*.<domain>.* 
  [Regex filters made by](https://github.com/nickspaargaren/pihole-google/issues/7) [@scoobydom0](https://github.com/scoobydom0)
  
## Sites you may want to whitelist
>recaptcha.google.com