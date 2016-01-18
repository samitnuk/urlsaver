## URL saver
Saving URLs (and other text) from browser address bar.

_This repository created, because with it for me will be easier to work from differ PCs. If somebody will read this I must to say sorry for my English, but I will be glad for any comments :)_

I realy like how [saved.io](http://saved.io/) works. And it has very minimalistic design.
Because I want to learn Python (like a hobby) and how it can be used for web, I will try to make something similar to __saved.io__ using __Flask__, __Bootstrap__ and many pieces of __Python__ code from the interenet.

For now I can test all this just on my PC, but in this app I will use URL "urlsaver.ua" instead of "127.0.0.1".

So this app should work next way:
* if you add "urlsaver.ua" before any path in browser, it will save path (for example: "urlsaver.ua/https://translate.google.com.ua" save path https://translate.google.com.ua).
* if you add "groupname.urlsaver.ua" before any path in browser, it will save path and add it to group "groupname" - so subdomain will mean group for path (for example: "translator.urlsaver.ua/https://translate.google.com.ua" save path https://translate.google.com.ua to group "translator").

As a templates for this projest I will try to use some elements from very nice [DashGum](http://blacktie.co/2014/07/dashgum-free-dashboard/) admin panel.

---


###### Notes:
For testing this app on PC to etc/hosts should be added couple lines similar to these:
```
127.0.0.1		urlsaver.ua
127.0.0.1		groupname1.urlsaver.ua
127.0.0.1		groupname2.urlsaver.ua
...
127.0.0.1		groupnameN.urlsaver.ua
```
All subdomains (from "groupname1" to "groupnameN") will work on local PC and all other will not. But any subdomains will work on real server.