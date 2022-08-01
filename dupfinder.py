"""Different algorithms for finding duplicates"""
from itertools import groupby

KEYS = [
    "name",
    "notes",
    "favorite",
    "folderId",
    "organizationId",
    "reprompt",
    "totp",
    "type",
    "username",
    "password",
]


def hashable(login) -> tuple:
    """Hashable tuple of a login"""
    return tuple(
        [
            *[login[key] for key in KEYS],
            "\n".join(login["domains"]),
            "\n".join(
                f'{field["name"]}: {field["value"]}'
                for field in login.get("fields", [])
            ),
        ]
    )


def identical_duplicates(logins):
    """Get a dictionary of hash key and its identical duplicate (always last one)"""
    seen = set()
    dupes = {}
    for login in logins:
        tup = hashable(login)
        if tup in seen:
            dupes[tup] = login
        else:
            seen.add(tup)
    return dupes


def dups_uris(items, func):
    """Duplicates by set and find"""
    uris = set()
    for item in items:
        if item.get("fields", None):
            item["fields"] = [
                field
                for field in item["fields"]
                if field.get("name", None) and field.get("value", None)
            ]
        item["domains"] = []
        for uri in func(item):
            item["domains"].append(uri)
            uris.add(uri)

    duplicates = {}
    for uri in sorted(list(uris)):
        filtered = [e for e in items if uri in e.get("domains", [])]
        if len(filtered) > 1:
            duplicates[uri] = filtered
    return duplicates
