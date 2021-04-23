#! /usr/bin/env python3
"""Find duplicates from bitwarden export and present them in as a html website"""
# %% Imports
import json
import os
import re
import sys
import webbrowser

from dupfinder import dups_uris

# %% Select a file
if sys.argv[1:]:
    filename = sys.argv[1]
else:
    try:
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename
        Tk().withdraw()  # Hide empty window
        filename = askopenfilename(**{
            "title": "Select your Bitwarden export file (.json extension)",
            "filetypes": [("Bitwarden export", "*.json")],
            "initialdir": os.getcwd()
        })
    except ImportError:
        print("You don't have tkinter installed install it with `pip install tkinter`")
        print("Otherwise provide path to bitwarden export as an argument")
        print("Example: `python bitwarden.py bitwarden_export.json`")
        sys.exit(1)

# %% Get items and folders from file
with open(filename, encoding="utf-8") as f:
    data = json.load(f)
    folders = data.get("folders", [])
    items = data.get("items", [])

# %% Expand login descendats (make username & password top level)
for row in items:
    for key, val in row.get("login", {}).items():
        row[key] = val

# %% Filter for accounts
items = [i for i in items if i.get("type") == 1]


# %% Define uri cleaning function
def domains(entry):
    """Get domains from login"""
    def transform(url):
        match = re.match(r"(\w+:\/\/)?([\w.]+)(\/?.*)", url)
        if match:
            return ".".join(match.group(2).split(".")[-2:])
        return ""
    return set(filter(None, (transform(uri.get("uri")) for uri in entry.get("uris", []))))


# %% Write object to file
duplicates = dups_uris(items, func=domains)

with open("logins.js", "w", encoding='utf-8') as f:
    data = json.dumps(duplicates, sort_keys=True)
    f.write("const logins = JSON.parse('")
    f.write(re.escape(data))
    f.write("')")

# %% Open in visual html file
webbrowser.open("index.html")
