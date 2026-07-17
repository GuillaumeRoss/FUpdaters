#!/usr/bin/env python3
"""Render the README app table + footnotes from apps.json and the profile.

The README's prose is hand-written. Two regions are generated and must not be
edited by hand:

  <!-- APPS_TABLE:BEGIN --> ... <!-- APPS_TABLE:END -->
  <!-- FOOTNOTES:BEGIN --> ... <!-- FOOTNOTES:END -->

Data sources:
  - FUpdaters.mobileconfig : the authoritative preference domains + keys/values
    (so the table can never drift from what the profile actually sets).
  - apps.json              : names, status, docs, coverage, footnote wiring.

Usage:
  python3 scripts/render_readme.py          # rewrite the two regions in README.md
  python3 scripts/render_readme.py --check   # exit 1 if README.md is out of date
"""
import json
import plistlib
import re
import sys

SPARKLE = "[Sparkle](https://sparkle-project.org/documentation/)"
PROFILE = "FUpdaters.mobileconfig"
DATA = "apps.json"
README = "README.md"

CASK = "https://formulae.brew.sh/cask/%s"
INST = "https://github.com/Installomator/Installomator/blob/main/fragments/labels/%s.sh"
FLEET = "https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/%s/darwin.json"


def slug_of(payload):
    return payload["PayloadIdentifier"].split("disable-updaters.")[-1]


def render_value(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def render_keys(mcx):
    parts = []

    def walk(prefix, d):
        for k, v in d.items():
            if isinstance(v, dict):
                walk(prefix + k + ".", v)
            else:
                parts.append(f"`{prefix}{k}={render_value(v)}`")

    walk("", mcx)
    return ", ".join(parts)


def footrefs(keys):
    return "".join(f" [^{k}]" for k in keys)


def coverage_cell(value, template, foot=""):
    if value is True:
        return "X" + foot
    if isinstance(value, str) and value:
        return f"[X]({template % value})" + foot
    return "—"


def build(profile, data):
    apps = {a["slug"]: a for a in data["apps"]}
    prof_slugs = [slug_of(p) for p in profile["PayloadContent"]]

    missing = [s for s in prof_slugs if s not in apps]
    extra = [s for s in apps if s not in prof_slugs]
    if missing or extra:
        raise SystemExit(
            "apps.json and the profile are out of sync:\n"
            + (f"  in profile, missing from apps.json: {missing}\n" if missing else "")
            + (f"  in apps.json, missing from profile: {extra}\n" if extra else "")
            + "Add/remove the entry so both match."
        )

    rows = ["| App | Preference domain | Key(s) set | Status | Docs | Alectrona | Fleet | Installomator | Cask |",
            "|-----|-------------------|------------|--------|------|:---------:|:-----:|:------------:|:----:|"]
    used = []  # footnote keys, in order of first use
    for p in profile["PayloadContent"]:
        s = slug_of(p)
        a = apps[s]
        domain = list(p["PayloadContent"].keys())[0]
        mcx = p["PayloadContent"][domain]["Forced"][0]["mcx_preference_settings"]

        status = a["status"] + footrefs(a.get("statusFootnotes", []))
        docs = a.get("docs") or (SPARKLE if a["status"] == "Sparkle" else "—")
        cov = a["coverage"]
        covfn = a.get("coverageFootnotes", {})
        for k in a.get("statusFootnotes", []) + [x for v in covfn.values() for x in v]:
            if k not in used:
                used.append(k)

        cells = [
            a["name"], f"`{domain}`", render_keys(mcx), status, docs,
            "X" if cov["alectrona"] else "—",
            coverage_cell(cov["fleet"], FLEET, footrefs(covfn.get("fleet", []))),
            coverage_cell(cov["installomator"], INST, footrefs(covfn.get("installomator", []))),
            coverage_cell(cov["cask"], CASK, footrefs(covfn.get("cask", []))),
        ]
        rows.append("| " + " | ".join(cells) + " |")

    footnotes = [f"[^{k}]: {data['footnotes'][k]}" for k in used]
    return "\n".join(rows), "\n".join(footnotes)


def replace_region(text, name, content):
    begin, end = f"<!-- {name}:BEGIN -->", f"<!-- {name}:END -->"
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"marker {begin} ... {end} not found in {README}")
    return pattern.sub(f"{begin}\n{content}\n{end}", text)


def main(argv):
    check = "--check" in argv[1:]
    profile = plistlib.load(open(PROFILE, "rb"))
    data = json.load(open(DATA))
    table, footnotes = build(profile, data)

    current = open(README).read()
    updated = replace_region(current, "APPS_TABLE", table)
    updated = replace_region(updated, "FOOTNOTES", footnotes)

    if check:
        if updated != current:
            print(f"{README} is out of date. Run: python3 scripts/render_readme.py",
                  file=sys.stderr)
            return 1
        print(f"{README}: up to date")
        return 0

    open(README, "w").write(updated)
    print(f"{README}: rendered {len(data['apps'])} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
