#!/usr/bin/env python3
"""Operation health check. Run FIRST in every automated cycle:
    python3 ops/tools/healthcheck.py [--heartbeat "note"]

Exists because of the Sep 1-17 blackout: a scheduled Routine fired ~60 times
reporting SUCCEEDED while running connectorless -- no Gmail, no sends, no
commits, no trace. Sixteen days of nothing looked identical to sixteen days of
working. This makes that impossible: every run must leave a heartbeat line in
the repo, so silence becomes visible in git history instead of invisible.

Exit 0 = healthy. Exit 1 = degraded (details on stdout). Never blocks work;
it reports. The caller is responsible for acting on a degraded result.
"""
import csv, sys, json, datetime, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
HEARTBEAT = ROOT / "ops/heartbeat.log"
TODAY = datetime.date.today()
problems, notes = [], []

def days_since(d):
    return (TODAY - datetime.date.fromisoformat(d)).days

# 1. Log freshness
log = ROOT / "ops/log.md"
if log.exists():
    import re
    days = re.findall(r"^## Day \d+.*?([A-Z][a-z]{2} \d{1,2}, \d{4})", log.read_text(), re.M)
    if days:
        try:
            last = datetime.datetime.strptime(days[-1], "%b %d, %Y").date()
            age = (TODAY - last).days
            notes.append(f"log last entry: {last} ({age}d ago)")
            if age > 1:
                problems.append(f"LOG STALE: {age} days since last entry")
        except ValueError:
            notes.append("log last entry: unparseable date")

# 2. Last actual send, per the tracker
rows = list(csv.DictReader((ROOT / "ops/prospects.csv").open()))
dates = sorted(r["sent_date"] for r in rows if r.get("sent_date"))
if dates:
    age = days_since(dates[-1])
    notes.append(f"last recorded send: {dates[-1]} ({age}d ago)")
    if age > 2:
        problems.append(f"NO SENDS in {age} days -- pipeline is idle")
else:
    problems.append("NO SENDS ever recorded")

# 3. Heartbeat freshness -- catches blind runs that left no other trace
if HEARTBEAT.exists():
    lines = [l for l in HEARTBEAT.read_text().splitlines() if l.strip()]
    if lines:
        stamp = lines[-1].split()[0]
        try:
            age = days_since(stamp[:10])
            notes.append(f"last heartbeat: {stamp[:10]} ({age}d ago)")
            if age > 1:
                problems.append(f"HEARTBEAT STALE: {age} days -- cycle not running")
        except ValueError:
            pass
else:
    problems.append("NO HEARTBEAT FILE -- cycle has never confirmed a healthy run")

# 4. Cap sanity: is today covered by an explicit ramp entry?
cfg = json.loads((ROOT / "ops/tools/cap.json").read_text())
key = TODAY.isoformat()
if key in cfg:
    notes.append(f"cap today: {cfg[key]} (explicit)")
else:
    notes.append(f"cap today: {cfg.get('default')} (FALLTHROUGH to default -- ramp file is stale)")
    problems.append("CAP FALLTHROUGH: no explicit entry for today; update cap.json")

# 5. Tracker integrity
from collections import Counter
counts = Counter(r["status"] for r in rows)
notes.append("tracker: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
dnc = ROOT / "ops/outreach/do-not-contact.txt"
blocked = {l.strip().lower() for l in dnc.read_text().splitlines()
           if l.strip() and not l.startswith("#")} if dnc.exists() else set()
leaked = [r["email"] for r in rows
          if r["email"].strip().lower() in blocked and r["status"] not in ("dead",)]
if leaked:
    problems.append(f"DNC LEAK: {leaked} on do-not-contact but not marked dead")

print("=== Loya Media health check ===")
for n in notes:
    print("  ·", n)
if problems:
    print("\nDEGRADED:")
    for p in problems:
        print("  !", p)
else:
    print("\nHEALTHY")

if "--heartbeat" in sys.argv:
    i = sys.argv.index("--heartbeat")
    note = sys.argv[i + 1] if len(sys.argv) > i + 1 else "cycle ran"
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    state = "DEGRADED" if problems else "OK"
    with HEARTBEAT.open("a") as f:
        f.write(f"{ts} {state} {note}\n")
    print(f"\nheartbeat written: {ts} {state} {note}")

sys.exit(1 if problems else 0)
