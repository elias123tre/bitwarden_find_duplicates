#! /usr/bin/env python3
"""Find duplicates from bitwarden export and present them in as a html website"""
# %% Imports
import json
import os
from pathlib import Path
import re
import sys
import webbrowser

from dupfinder import dups_uris, identical_duplicates

# %% Select a file
if sys.argv[1:]:
    filename = sys.argv[1]
else:
    try:
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename

        Tk().withdraw()  # Hide empty window
        filename = askopenfilename(
            title="Select your Bitwarden export file (.json extension)",
            filetypes=[("Bitwarden export", "*.json")],
            initialdir=os.getcwd(),
        )
    except ImportError:
        print(
            "You don't have tkinter installed or it is not working, "
            "install it with `pip install tkinter` or `pip3 install tkinter`"
        )
        print("Otherwise provide path to bitwarden export as an argument")
        print("Example: `python bitwarden.py bitwarden_export.json`")
        sys.exit(1)
if not filename:
    print("No file selected. Quitting.")
    sys.exit(1)

# %% Get items and folders from file
with open(filename, encoding="utf-8") as f:
    data = json.load(f)
    folders = {
        folder.get("id"): folder.get("name")
        for folder in data.get("folders", [])
        if folder.get("id")
    }
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
        if not url:
            return ""
        match = re.match(r"(\w+:\/\/)?([\w.]+)(\/?.*)", url)
        if match:
            return ".".join(match.group(2).split(".")[-2:])
        return ""

    return set(
        filter(None, (transform(uri.get("uri", "")) for uri in entry.get("uris", [])))
    )


# %% Write object to file
duplicates = dups_uris(items, func=domains)

identical = {}
for domain in duplicates.values():
    identical.update(identical_duplicates(domain))

with open("logins.js", "w", encoding="utf-8") as f:
    ident_dupes = json.dumps(list(identical.values()), sort_keys=True)
    f.write(f"const identical = {ident_dupes}")
    f.write("\n\n")
    data = json.dumps(duplicates, sort_keys=True)
    f.write(f"const logins = {data}")
    f.write("\n\n")
    folders_str = json.dumps(folders, sort_keys=True)
    f.write(f"const folders = {folders_str}")

# %% Try open in visual html file
print("Trying to open the GUI your preferred browser...")
filepath = Path("index.html").resolve().as_uri()
print(f"If it doesn't open by itself, open {filepath} manually in any browser")

webbrowser.open(filepath)
