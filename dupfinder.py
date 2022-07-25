"""Different algorithms for finding duplicates"""
from itertools import groupby


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
