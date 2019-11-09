# Sublime Text 3 (and 2) SendToPasteBin Plugin

Sublime Text 3 (and 2) plugin uploads code to Pastebin.com directly from the editor, with the correct syntax highlighting.

## Usage

Use shortcuts or commands in the command prompt (prefix `SendToPasteBin`).

## Shortcuts

-   `ctrl+alt+c`: copy the current selection in Pastebin.com. The resulting Url will be copied to your clipboard
-   `ctrl+alt+shift+c`: same as `ctrl+alt+c`, but with a custom name of resulting pasted file

## Configuration

`SendToPasteBin.sublime-settings`:

```
{
    // See https://pastebin.com/api for api key information.
    "api_dev_key": "your key",
    "api_user_key": "your key",

    // Choose privacy for pastes:
    // 0 = Public, 1 = Unlisted, 2 = Private
    "paste_privacy": 0,

    // Choose expiration for pastes:
    // N = Never, 10M = 10 Minutes, 1H = 1 Hour, 1D = 1 Day, 1W = 1 Week, 2W = 2 Weeks, 1M = 1 Month
    "paste_expiration": "1D",

    // Choose url type:
    // "default", "raw"
    "paste_url_type": "default"
}
```

To get the dev_key, go to https://pastebin.com/api .

To generate the user_key, go to https://pastebin.com/api/api_user_key.html and fill you dev_key and account info.

## Installation

Install through package control or clone this repo in your `Sublime Packages/` folder with the name `SendToPasteBin`
