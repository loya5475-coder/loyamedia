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
                                   exists -- both Aug-26 bounces had live MX).
                                   Requires the dnspython package (see
                                   ops/tools/requirements.txt) -- if it is
                                   missing this blocks with a clear tooling
                                   error, it never reports a false "dead domain".
  5. cold-start guard           -> if the mailbox has been silent >=7 days, the
                                   effective cap is clamped to 3 regardless of
                                   cap.json. Resuming at full volume after a
                                   silence reads as account compromise.
  6. physical mailing address   -> hard block if unavailable. CAN-SPAM requires
                                   one in every commercial email (see
                                   templates.md signature block). Read from
                                   gitignored ops/private/sender-identity.txt,
                                   falling back to the LOYAMEDIA_MAILING_ADDRESS
                                   env var. The gitignored file does NOT survive
                                   a fresh clone -- an unattended/scheduled run
                                   in a fresh container has no address unless
                                   the environment sets that env var.
  7. --source-verbatim flag     -> sender attests address was copied verbatim
                                   from the brand's own page; absent = block
"""
import csv, os, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]

def sender_address():
    f = ROOT / "ops/private/sender-identity.txt"
    if f.exists():
        text = f.read_text().strip()
        if text:
            return text
    return os.environ.get("LOYAMEDIA_MAILING_ADDRESS", "").strip() or None


# Placeholder tokens. Added Oct 5 after a near-miss: the documented example
# address ("1234 Example St, Las Cruces, NM 88001") was pasted into the env var
# verbatim, and this gate returned CLEAR for three real prospects because it
# only checked that SOME address existed. A fabricated address in a CAN-SPAM
# footer is a legal violation and torches sender reputation, so "is it present"
# was never a sufficient test. It has to be plausibly real.
PLACEHOLDER_TOKENS = (
    "example", "placeholder", "your address", "youraddress", "street name",
    "123 main", "1234 main", "lorem", "fake", "dummy", "tbd", "xxx",
    "<", ">", "{", "}", "[", "]",
)


def address_problem(addr):
    """Return a reason string if addr is unusable, else None."""
    if not addr:
        return ("no physical mailing address available -- "
                "ops/private/sender-identity.txt is missing and "
                "LOYAMEDIA_MAILING_ADDRESS is unset. CAN-SPAM requires a real "
                "postal address in every commercial email. Do not send without "
                "one; do not fabricate one. This needs Jose to set the env var "
                "(the gitignored file does not survive a fresh clone).")

    low = addr.lower()
    for tok in PLACEHOLDER_TOKENS:
        if tok in low:
            return (f"mailing address looks like a PLACEHOLDER (matched {tok!r}), "
                    f"not a real address. Sending a fabricated address in a "
                    f"CAN-SPAM footer is illegal and would burn the domain. Ask "
                    f"Jose to set LOYAMEDIA_MAILING_ADDRESS to his actual "
                    f"mailing address. Never substitute an example.")

    import re
    if not re.search(r"\b\d{5}(-\d{4})?\b", addr):
        return ("mailing address has no 5-digit ZIP code -- it does not look "
                "like a deliverable US address. Do not send; do not invent one.")
    if not re.search(r"\b[A-Z]{2}\b", addr):
        return ("mailing address has no 2-letter state code -- it does not look "
                "like a deliverable US address. Do not send; do not invent one.")
    if not re.search(r"\d", addr.split()[0]):
        return ("mailing address does not start with a street number -- "
                "verify it is a real, deliverable address before sending.")
    if len(addr) < 15:
        return (f"mailing address is only {len(addr)} characters -- too short to "
                f"be a complete postal address. Do not send.")
    return None
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
                # Follow-ups. Fixed Oct 7: this was a bare hard block, which
                # meant the documented 3-touch sequence (T2 at +4 days, T3 at
                # +9) could never actually be sent -- the gate refused every
                # follow-up to a row it had just marked `sent`. It also stranded
                # the 16 `cold` rows that policy says get exactly ONE breakup
                # touch. `inherited` rows already had a guarded override
                # (--bridge-in-thread) and these never got the equivalent.
                #
                # This is NOT a loosening: a first cold touch is still blocked
                # without the flag, touch >= 3 is still closed forever, dead is
                # still absolute, and the address/MX/cap checks all still run.
                # It only permits the in-thread follow-up the playbook already
                # prescribes, and only when the caller says so explicitly.
                t = int(r.get("touch") or 0)
                if t >= 3:
                    fail(f"{email} already at {t} touches -- thread is closed "
                         f"forever. Nothing after T3.")
                if "--followup-in-thread" not in sys.argv:
                    fail(f"{email} already contacted (status={r['status']}, touch {t}). "
                         f"A second cold first-touch would be a stranger pitching twice "
                         f"from one address. If this is the in-thread follow-up the "
                         f"playbook prescribes (T2 at +4 days, T3 breakup at +9), send it "
                         f"as a REPLY in the existing thread and re-run with "
                         f"--followup-in-thread.")
                print(f"NOTE: {r['status']} row at touch {t}; this send is touch {t+1} "
                      f"and MUST be a reply in the existing thread")
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
    except ImportError:
        fail(f"dnspython not installed in this environment -- "
             f"pip install -r ops/tools/requirements.txt. This is a tooling gap, "
             f"NOT evidence {domain} is dead -- do not mark this prospect dead "
             f"based on this failure.")
    try:
        dns.resolver.resolve(domain, "MX", lifetime=8)
    except Exception as e:
        # Control probe, added Oct 9. If a domain that certainly has MX records
        # also fails, the resolver is broken and this says nothing about the
        # prospect. Without this probe the gate reported "dead domain" for every
        # address -- including gmail.com -- and the scheduled runs on Oct 8 and
        # Oct 9 sent nothing while blaming the prospects.
        dns_broken = False
        try:
            dns.resolver.resolve("gmail.com", "MX", lifetime=8)
        except Exception:
            dns_broken = True

        if dns_broken:
            fail(f"DNS IS UNAVAILABLE IN THIS ENVIRONMENT -- the control probe for "
                 f"gmail.com also failed ({type(e).__name__}). This says NOTHING about "
                 f"{domain}; do NOT mark this prospect dead and do NOT re-source the "
                 f"address. The MX gate cannot run here. Causes seen: the sandbox "
                 f"resolver returning NXDOMAIN for everything, and the network policy "
                 f"denying DNS-over-HTTPS (dns.google:443 -> 403). Escalate the policy "
                 f"decision -- do not self-authorize sending with the MX check skipped.")
        fail(f"no MX record for {domain} ({type(e).__name__}) -- dead domain. "
             f"(DNS itself is working: the gmail.com control probe succeeded.)")

    problem = address_problem(sender_address())
    if problem:
        fail(problem)

    if "--source-verbatim" not in sys.argv:
        fail("missing --source-verbatim: attest the address was copied "
             "verbatim from the brand's own site, then re-run")

    print(f"CLEAR: {email} ({sent_today}/{cap} sent today, MX ok)")

if __name__ == "__main__":
    main()
