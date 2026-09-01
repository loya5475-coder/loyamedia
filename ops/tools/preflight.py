#!/usr/bin/env python3
"""Pre-send gate. Run BEFORE every outreach email:
    python3 ops/tools/preflight.py <email> [--source-verbatim]

Exits 0 = clear to send. Exits 1 = BLOCKED (reason on stdout).
Layers, in order:
  1. do-not-contact list        -> hard block, never overridable
  2. already contacted (tracker)-> hard block (dedupe; protects reputation)
  3. daily send cap (ramped)    -> from ops/tools/cap.json; hard block
  4. MX record on domain        -> hard block if absent (catches dead domains
                                   ONLY; a live MX does not prove the mailbox
                                   exists -- both Aug-26 bounces had live MX)
  5. --source-verbatim flag     -> sender attests address was copied verbatim
                                   from the brand's own page; absent = block
"""
import csv, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
def daily_cap():
    """Ramped cap from ops/tools/cap.json (UTC date key), default 30."""
    import json
    cfg = json.loads((ROOT / "ops/tools/cap.json").read_text())
    return int(cfg.get(datetime.date.today().isoformat(), cfg.get("default", 30)))
DAILY_CAP = None

def fail(msg):
    print(f"BLOCKED: {msg}"); sys.exit(1)

def main():
    if len(sys.argv) < 2:
        fail("usage: preflight.py <email> [--source-verbatim]")
    email = sys.argv[1].strip().lower()
    domain = email.split("@")[-1]

    dnc = ROOT / "ops/outreach/do-not-contact.txt"
    if dnc.exists():
        entries = {l.strip().lower() for l in dnc.read_text().splitlines()
                   if l.strip() and not l.startswith("#")}
        if email in entries or domain in entries:
            fail(f"{email} is on the do-not-contact list")

    tracker = ROOT / "ops/prospects.csv"
    today = datetime.date.today().isoformat()
    sent_today = 0
    if tracker.exists():
        rows = list(csv.DictReader(tracker.open()))
        for r in rows:
            e = (r.get("email") or "").strip().lower()
            if e == email and r.get("status") == "dead":
                fail(f"{email} is dead ({r.get('outcome') or 'bounced/opt-out'})")
            if e == email and r.get("status") == "sent":
                fail(f"{email} already contacted (status=sent, touch {r.get('touch')})")
            if e == email and r.get("status") == "inherited":
                t = int(r.get("touch") or 0)
                if t >= 3:
                    fail(f"{email} inherited thread already at {t} touches -- closed")
                print(f"NOTE: inherited thread at touch {t}; this send is touch {t+1} and must reply IN-THREAD")
            if r.get("sent_date") == today:
                sent_today += 1
    cap = daily_cap()
    if sent_today >= cap:
        fail(f"daily cap reached ({sent_today}/{cap}); resume tomorrow")

    try:
        import dns.resolver
        dns.resolver.resolve(domain, "MX", lifetime=8)
    except Exception as e:
        fail(f"no MX record for {domain} ({type(e).__name__}) -- dead domain")

    if "--source-verbatim" not in sys.argv:
        fail("missing --source-verbatim: attest the address was copied "
             "verbatim from the brand's own site, then re-run")

    print(f"CLEAR: {email} ({sent_today}/{cap} sent today, MX ok)")

if __name__ == "__main__":
    main()
