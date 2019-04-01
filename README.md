# Purge Google from your network!

Protect yourself from Google's surveillance by using this blocklist!

Feel free to criticize my blocklist to make it better and better.
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

# Youtube Advertisements Regex
>_^r.+\googlevideo.com$_

NOTE: This is supposed to prevent these domains to be
loaded not only on youtube, but on all over the web and,
since I'm trying to completely block google in my home,
I don't care if youtube is broken.
I'll may work on an efficient regex for this purpose.

# Sites you may want to whitelist
>0.0.0.0 recaptcha.google.com
