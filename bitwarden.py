#!/usr/bin/python3
"""Find duplicates from bitwarden export and present them in as a html website"""
# %% Imports
import json
import os
import re
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from dupfinder import dups_uris

# %% Select a file
Tk().withdraw()  # Hide empty window
filename = askopenfilename(**{
    "title": "Select your Bitwarden export file (.json extension)",
    "filetypes": [("Bitwarden export", "*.json")],
    "initialdir": os.getcwd()
})
if not filename:
    print("Error: no file selected.")
    sys.exit(1)

# %% Get items and folders from file
with open(filename, encoding="utf-8") as f:
    data: dict[list[dict]] = json.load(f)
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
            return ".".join(match.group(2).removeprefix("www.").split(".")[-2:])
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
os.startfile("index.html")
