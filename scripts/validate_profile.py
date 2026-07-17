#!/usr/bin/env python3
"""Validate FUpdaters configuration profile(s).

Checks each .mobileconfig is a well-formed plist and structurally sound as an
Apple configuration profile:

  - parses as a plist
  - top-level PayloadType == "Configuration"
  - required top-level keys are present
  - every sub-payload has the required keys
  - all PayloadUUIDs are unique and well-formed
  - all PayloadIdentifiers are unique

Usage:
  python3 scripts/validate_profile.py [file.mobileconfig ...]

With no arguments it validates every *.mobileconfig in the repo root.
Exits non-zero (and prints ERROR lines) if anything fails.
"""
import glob
import plistlib
import re
import sys

UUID_RE = re.compile(
    r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$"
)
REQUIRED_TOP = ["PayloadType", "PayloadVersion", "PayloadIdentifier", "PayloadUUID"]
REQUIRED_PAYLOAD = ["PayloadType", "PayloadVersion", "PayloadIdentifier", "PayloadUUID"]


def validate(path):
    errors = []
    try:
        with open(path, "rb") as f:
            data = plistlib.load(f)
    except Exception as e:  # malformed XML or not a plist
        return [f"{path}: not a valid plist: {e}"]

    if not isinstance(data, dict):
        return [f"{path}: top-level plist object must be a dict"]

    if data.get("PayloadType") != "Configuration":
        errors.append(
            f"{path}: top-level PayloadType must be 'Configuration' "
            f"(got {data.get('PayloadType')!r})"
        )
    for k in REQUIRED_TOP:
        if k not in data:
            errors.append(f"{path}: missing top-level key {k}")

    uuids = {}
    idents = {}
    top_uuid = data.get("PayloadUUID")
    if top_uuid:
        uuids[top_uuid] = "<top-level>"
    top_ident = data.get("PayloadIdentifier")
    if top_ident:
        idents[top_ident] = "<top-level>"

    payloads = data.get("PayloadContent", [])
    if not isinstance(payloads, list):
        errors.append(f"{path}: PayloadContent must be an array")
        payloads = []

    for i, p in enumerate(payloads):
        loc = f"payload #{i + 1}"
        if not isinstance(p, dict):
            errors.append(f"{path}: {loc} is not a dict")
            continue
        name = p.get("PayloadDisplayName", p.get("PayloadIdentifier", loc))

        for k in REQUIRED_PAYLOAD:
            if k not in p:
                errors.append(f"{path}: {name}: missing key {k}")

        u = p.get("PayloadUUID")
        if u is not None:
            if not UUID_RE.match(str(u)):
                errors.append(f"{path}: {name}: PayloadUUID is not a valid UUID: {u}")
            elif u in uuids:
                errors.append(
                    f"{path}: duplicate PayloadUUID {u} ({name} and {uuids[u]})"
                )
            else:
                uuids[u] = name

        pid = p.get("PayloadIdentifier")
        if pid is not None:
            if pid in idents:
                errors.append(
                    f"{path}: duplicate PayloadIdentifier {pid} "
                    f"({name} and {idents[pid]})"
                )
            else:
                idents[pid] = name

    if not errors:
        print(f"{path}: OK ({len(payloads)} payloads)")
    return errors


def main(argv):
    paths = argv[1:] or sorted(glob.glob("*.mobileconfig"))
    if not paths:
        print("no .mobileconfig files found", file=sys.stderr)
        return 1
    all_errors = []
    for p in paths:
        all_errors += validate(p)
    for e in all_errors:
        print("ERROR: " + e, file=sys.stderr)
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
