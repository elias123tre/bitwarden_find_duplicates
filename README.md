# Bitwarden Find Duplicates

Find duplicate logins based on domain, from bitwarden export.
Open source for your safety, read through before executing.

## How to use

Run the `bitwarden.py` file:

```terminal
python bitwarden.py
```

Then choose your Bitwarden json export (needs to be unencrypted :c ) and it will open a nice looking website presenting the duplicates in your browser.

_or_

Specify file path manually:

```terminal
python bitwarden.py bitwarden_export.json
```

Where `bitwarden_export.json` is the path to your export.

## Requirements

- Python 3.7 at least
- Modern browser (tested with Firefox 88 and Chrome 86)

## Demonstration

![Demonstration](https://i.imgur.com/PlXPOCT.png)
