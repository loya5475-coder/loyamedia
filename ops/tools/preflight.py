#!/usr/bin/env python3
"""Pre-send gate. Run BEFORE every outreach email:
    python3 ops/tools/preflight.py <email> --source-verbatim [--bridge-in-thread]

Exits 0 = clear to send. Exits 1 = BLOCKED (reason on stdout).
Layers, in order:
  1. do-not-contact list        -> hard block, never overridable
  2. already contacted (tracker)-> hard block on status sent/cold/dead/inherited
                                   (dedupe; protects reputation). NOTE: any new
                                   status added to the tracker MUST be added here
                                   or already-contacted people become sendable.
  3. daily send cap (ramped)    -> from ops/tools/cap.json; hard block
  4. MX record on domain        -> hard block if absent (catches dead domains
                                   ONLY; a live MX does not prove the mailbox
                                   exists -- both Aug-26 bounces had live MX)
  5. cold-start guard           -> if the mailbox has been silent >=7 days, the
                                   effective cap is clamped to 3 regardless of
                                   cap.json. Resuming at full volume after a
                                   silence reads as account compromise.
  6. --source-verbatim flag     -> sender attests address was copied verbatim
                                   from the brand's own page; absent = block
"""
import csv, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
def daily_cap(rows=None):
    """Ramped cap from ops/tools/cap.json, clamped to 3 after a >=7 day silence.

    The clamp exists because cap.json's dated ramp goes stale: after the
    Sep 1-17 blackout every entry was in the past and today fell through to
    default=30, which would have meant 30 sends from a mailbox that had been
    dark for 17 days. The config can rot; this guard cannot.
    """
    import json
    cfg = json.loads((ROOT / "ops/tools/cap.json").read_text())
    cap = int(cfg.get(datetime.date.today().isoformat(), cfg.get("default", 10)))
    if rows:
        sent = sorted(r["sent_date"] for r in rows if r.get("sent_date"))
        if sent:
            idle = (datetime.date.today() - datetime.date.fromisoformat(sent[-1])).days
            if idle >= 7 and cap > 3:
                print(f"NOTE: mailbox idle {idle}d -- cold-start guard clamps cap {cap} -> 3")
                return 3
    return cap
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
    rows = []
    if tracker.exists():
        rows = list(csv.DictReader(tracker.open()))
        for r in rows:
            e = (r.get("email") or "").strip().lower()
            if e == email and r.get("status") == "dead":
                fail(f"{email} is dead ({r.get('outcome') or 'bounced/opt-out'})")
            if e == email and r.get("status") in ("sent", "cold"):
                fail(f"{email} already contacted (status={r['status']}, touch {r.get('touch')})")
            if e == email and r.get("status") == "inherited":
                t = int(r.get("touch") or 0)
                if t >= 3:
                    fail(f"{email} inherited thread already at {t} touches -- closed")
                if "--bridge-in-thread" not in sys.argv:
                    fail(f"{email} is an INHERITED thread at touch {t}. They already heard "
                         f"from this mailbox. A cold first touch would be the second "
                         f"stranger-pitch from one address. Send an in-thread bridge (T1b) "
                         f"and re-run with --bridge-in-thread to confirm.")
                print(f"NOTE: inherited thread at touch {t}; this send is touch {t+1} "
                      f"and MUST be a reply in the existing thread")
            if r.get("sent_date") == today:
                sent_today += 1
    cap = daily_cap(rows)
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
