#!/usr/bin/env python3
"""fupdaters — cut a FUpdaters profile down to the apps your patching tools cover.

The full FUpdaters.mobileconfig disables the built-in updater for every app it
knows about. You should only disable an app's updater if *something else* keeps
it patched. This tool trims the profile to just the apps covered by the patching
tool(s) you actually run.

Coverage lives in apps.json (keyed by the payload slug). Pick the sources you
have; an app is kept if ANY of them covers it (because any one of your tools will
keep it up to date).

Examples
--------
  # You run Fleet. Keep only apps Fleet maintains:
  python3 fupdaters.py --fleet > MyProfile.mobileconfig

  # You run Homebrew and Alectrona Patch. Keep anything either one covers:
  python3 fupdaters.py --cask --alectrona -o MyProfile.mobileconfig

  # Keep anything covered by at least one known source:
  python3 fupdaters.py --any -o MyProfile.mobileconfig

  # Just show the coverage matrix, don't write a profile:
  python3 fupdaters.py --list

Nothing to install — this only uses Python 3 (already on any Mac with the
Command Line Tools). It never modifies the input profile; it writes a new one.
"""
import argparse
import json
import plistlib
import sys

SOURCES = ["fleet", "alectrona", "installomator", "cask"]
DEFAULT_INPUT = "FUpdaters.mobileconfig"
DEFAULT_DATA = "apps.json"


def load_data(path):
    with open(path, "rb") as f:
        return {a["slug"]: a for a in json.load(f)["apps"]}


def slug_of(payload):
    ident = payload.get("PayloadIdentifier", "")
    return ident.split("disable-updaters.")[-1] if "disable-updaters." in ident else None


def covered(app, sources):
    """True if the app is covered by ANY of the selected sources."""
    cov = app.get("coverage", {})
    return any(cov.get(s) for s in sources)


def do_list(profile, data, sources):
    mark = lambda v: " X " if v else " · "
    hdr = f"{'App':28} " + " ".join(f"{s[:5]:^5}" for s in SOURCES) + "  kept?"
    print(hdr)
    print("-" * len(hdr))
    kept = 0
    for p in profile["PayloadContent"]:
        slug = slug_of(p)
        app = data.get(slug)
        if not app:
            print(f"{(p.get('PayloadDisplayName') or slug or '?'):28} (not in {DEFAULT_DATA})")
            continue
        cov = app["coverage"]
        keep = covered(app, sources)
        kept += keep
        row = f"{app['name']:28} " + " ".join(mark(cov.get(s)) for s in SOURCES)
        print(row + f"   {'yes' if keep else 'no'}")
    print("-" * len(hdr))
    print(f"{kept} of {len(profile['PayloadContent'])} payloads match: {', '.join(sources)}")


def do_filter(profile, data, sources, out):
    unknown = [slug_of(p) or "<no slug>"
               for p in profile["PayloadContent"] if slug_of(p) not in data]
    if unknown:
        sys.exit(
            f"error: these profile payloads have no entry in {DEFAULT_DATA}: "
            + ", ".join(unknown)
            + "\n(the data file has drifted from the profile — fix before filtering)"
        )
    kept = [p for p in profile["PayloadContent"]
            if covered(data[slug_of(p)], sources)]
    result = dict(profile)
    result["PayloadContent"] = kept
    label = ", ".join(s.capitalize() for s in sources)
    if "PayloadDisplayName" in result:
        result["PayloadDisplayName"] += f" ({label})"
    if "PayloadDescription" in result:
        result["PayloadDescription"] += f" Filtered to apps covered by: {label}."

    blob = plistlib.dumps(result)
    if out is None or out == "-":
        sys.stdout.buffer.write(blob)
    else:
        with open(out, "wb") as f:
            f.write(blob)
    n = len(result["PayloadContent"])
    print(
        f"kept {n} of {len(profile['PayloadContent'])} payloads "
        f"(sources: {label})" + (f" -> {out}" if out and out != '-' else ""),
        file=sys.stderr,
    )


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="fupdaters.py",
        description="Trim FUpdaters.mobileconfig to the apps your patching tools cover.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Examples", 1)[1],
    )
    ap.add_argument("-i", "--input", default=DEFAULT_INPUT,
                    help=f"profile to read (default: {DEFAULT_INPUT})")
    ap.add_argument("-o", "--output", default="-",
                    help="write filtered profile here (default: stdout)")
    ap.add_argument("--data", default=DEFAULT_DATA,
                    help=f"coverage data file (default: {DEFAULT_DATA})")
    ap.add_argument("--any", action="store_true",
                    help="keep apps covered by at least one known source")
    for s in SOURCES:
        ap.add_argument(f"--{s}", action="store_true",
                        help=f"you run {s}: keep apps it covers")
    ap.add_argument("--list", action="store_true",
                    help="print the coverage matrix and exit (no profile written)")
    args = ap.parse_args(argv)

    selected = [s for s in SOURCES if getattr(args, s)]
    if args.any:
        selected = list(SOURCES)

    try:
        profile = plistlib.load(open(args.input, "rb"))
    except Exception as e:
        ap.error(f"could not read profile {args.input!r}: {e}")
    try:
        data = load_data(args.data)
    except Exception as e:
        ap.error(f"could not read data {args.data!r}: {e}")

    if args.list:
        do_list(profile, data, selected or SOURCES)
        return 0

    if not selected:
        ap.error(
            "pick at least one source to keep, e.g. --fleet or --cask "
            "(or --any for anything covered). Use --list to preview, -h for help."
        )

    do_filter(profile, data, selected, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
