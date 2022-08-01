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


def itemrepr(entry, keys=("name", "username", "password", "fields")):
    """Simple representation of login item"""
    rep = {k: v for k, v in entry.items() if k in keys}
    return rep


def dups_uris(items, func):
    """Duplicates by set and find"""
    uris = set()
    for item in items:
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


def dups_sort(items, func):
    """Duplicates by sorting and groupby
    ! DEPRECATED: NOT WORKING
    """
    items.sort(key=func)
    duplicates = [(k, [itemrepr(e) for e in g]) for k, g in groupby(items, key=func)]
    duplicates = [(dom, ents) for dom, ents in duplicates if len(ents) > 1]
    return duplicates


def dups_seen(items, func):
    """Duplicates by seen
    ! DEPRECATED: NOT WORKING
    """
    seen = set()
    for item in items:
        uris = func(item)
        if any(uri in seen for uri in uris):
            print("Duplicate:")
            yield {
                k: v
                for k, v in item.items()
                if k in ("name", "username", "password", "fields")
            }
            print()
        for uri in uris:
            seen.add(uri)
