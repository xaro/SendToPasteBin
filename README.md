Sublime Text 3 (and 2) SendToPasteBin Plugin
=============

Sublime Text 3 (and 2) plugin to upload code to pastebin.com directly from the editor with the correct syntax highlighting.

Usage
-------
Select text, hit the key binding (default `ctrl+alt+c`) and your PasteBin url will be copied to your clipboard, with the proper syntax highlight selected.

Configuration
-------

    "api_dev_key":  "your_key",
    "api_user_key": "your_key",

    // 0 = Public, 1 = Unlisted, 2 = Private
    "paste_privacy": 0,

    // N = Never, 10M = 10 Minutes, 1H = 1 Hour, 1D = 1 Day, 1W = 1 Week, 2W = 2 Weeks, 1M = 1 Month
    "paste_expire_date": "1D"

To get the dev_key, go to http://pastebin.com/api .

To generate the user_key, go to http://pastebin.com/api/api_user_key.html and fill you dev_key and account info.


Install through package control or clone this repo in your `Sublime Packages/` folder with the name `SendToPasteBin`