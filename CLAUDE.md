# Loya Media — ACTIVE AUTONOMOUS OPERATION

**Read this before doing anything else in this repo.**

A 30-day revenue challenge is running here: **Aug 26 → Sep 26, 2026.** Loya Media
is a real content agency (loyamedia.com) with a live site, a $150–$2,000 product
ladder, a business Gmail, and PayPal. The operation sells its copywriting by cold
outreach that delivers finished work before asking for money.

## First action in any session: check staleness

```bash
tail -40 ops/log.md          # what actually happened last
date -u                      # how long ago that was
```

Better: run the health check, which does this and more:

```bash
python3 ops/tools/healthcheck.py
```

**If it reports DEGRADED, the operation has gone dark. Resume immediately — do
not wait to be asked.** This has happened TWICE:
- Sep 2–5: a session closed, the scheduler died with it, 3 days lost.
- **Sep 1–17: 16 days lost.** A durable Routine fired ~60 times reporting
  SUCCESS while running with no Gmail connector. It sent nothing and left no
  trace, so dead days were indistinguishable from working days. Revenue impact:
  the entire back half of the challenge.

**The lesson is encoded, not remembered:** every automated run must end with
`healthcheck.py --heartbeat "<what it did>"` and commit. A run that leaves no
heartbeat did not happen.

## The resume sequence

1. **Bounces first.** Gmail `from:mailer-daemon OR from:postmaster newer_than:2d`.
   Any hard bounce → mark that prospect `dead` in `ops/prospects.csv`, halt *new*
   sends for 24h (in-thread follow-ups may continue), log it.
2. **Replies.** Gmail `in:inbox newer_than:3d -category:promotions`.
   - Pricing question → template T5 in `ops/outreach/templates.md`
   - Interested / yes → **send a PayPal invoice immediately**, then do the work
   - Opt-out → T6, add to `ops/outreach/do-not-contact.txt`, never contact again
3. **Follow-ups due** per `ops/prospects.csv`: T2 at +4 days, T3 at +9 days,
   in-thread. Nothing after T3 — three touches, then the thread closes.
4. **New outreach.** Research via WebSearch, write a real rewrite of that brand's
   actual copy *before* contact, then send T1.
5. **Books.** Update `ops/prospects.csv`, `ops/scoreboard.md`, `ops/log.md` with
   real numbers. Commit and push to `claude/ai-money-challenge-9uvred`.
6. **Heartbeat, always:** `python3 ops/tools/healthcheck.py --heartbeat "<one
   line on what this run actually did>"`, then commit and push. Runs that did
   nothing still write a heartbeat — that is the point.

**Before claiming a cycle ran: prove you can see.** Make one real Gmail call
first. If Gmail tools are unavailable you are BLIND: write a `BLIND RUN`
heartbeat, commit it, notify Jose, and stop. Never report success while blind.

## Sender identity and inherited threads (since Sep 1)

- All mail goes from **`josel@loyamedia.com`** (Workspace; SPF/DKIM/DMARC live).
- The mailbox previously ran a separate criticism-format campaign (57 threads,
  Aug 4–Sep 1). Those rows are `status=inherited` in the tracker. Touch ≥3 is
  closed forever. Touch <3 gets at most one **T1b bridge**, in-thread, with a
  real rewrite. Never a cold re-contact.
- Daily cap is ramped in `ops/tools/cap.json` (15/18/22/26 → 30). Preflight
  reads it and counts every send from the mailbox, whoever sent it.
- The ask is under A/B test: variant A ($800 catalog first) vs B ($150 blog
  post first). Alternate strictly, record the variant in the tracker.

## Hard rules — these are not style preferences

- **Never send without running the gate:**
  `python3 ops/tools/preflight.py <email> --source-verbatim` must print CLEAR.
  Inherited threads additionally need `--bridge-in-thread` (they already heard
  from this mailbox; a cold pitch would be the second stranger-pitch from one
  address).
- **If you add a status to `ops/prospects.csv`, add it to preflight's dedupe
  list.** Renaming `sent` → `cold` on Sep 18 silently made 16 already-contacted
  people sendable again until the regression test caught it.
- **Addresses only from a brand's own published page** — wholesale/sales/orders
  pages quoted verbatim in search results. Never a guessed `firstname@` pattern.
  That mistake produced a 22% bounce rate on day one.
- **Respect the ramped cap** in `ops/tools/cap.json`, and keep it current — its
  dated entries go stale and fall through to `default`. A **cold-start guard**
  in preflight clamps the cap to 3/day whenever the mailbox has been silent 7+
  days; that clamp is correct, never work around it. The mailbox is the entire
  revenue channel; a suspension ends the operation. No bursts >5/hour.
- **Every email carries a genuine rewrite written for that specific brand.** The
  moment this becomes a mail merge it stops working and stops being honest.
- **Rotate subject lines** per the pool in `ops/outreach/templates.md`.
- **Never fabricate a metric, testimonial, or result.** Every number in the
  scoreboard must be checkable against Gmail message IDs, bounce notices, or
  PayPal. Log the bad days too — a scoreboard nobody audits is worth nothing.
- **Never commit the mailing address.** It lives in gitignored
  `ops/private/sender-identity.txt` and is injected only at send time. This repo
  is public.
- **Do not scrape GitHub commit emails** for outreach. Considered and rejected
  on Aug 27 — see `ops/outreach/apollo-playbook.md`.

## Where things are

| Path | What |
|---|---|
| `ops/README.md` | Strategy, forecast, guardrails |
| `ops/log.md` | Daily record — the source of truth |
| `ops/scoreboard.md` | Current metrics |
| `ops/prospects.csv` | Every prospect, status, touch count |
| `ops/outreach/templates.md` | T1–T6 templates + deliverability rules |
| `ops/outreach/apollo-playbook.md` | Sourcing method, rejected approaches |
| `ops/tools/preflight.py` | Mandatory pre-send gate |
| `ops/tools/healthcheck.py` | Run first and last in every cycle; writes heartbeat |
| `ops/tools/cap.json` | Daily send caps (keep the ramp current) |
| `ops/heartbeat.log` | Proof-of-life per run. Gaps here = dead days |
| `ops/samples/` | Completed rewrites |

## Scheduler (since Sep 18 — send gap CLOSED)

**Live Routine: `trig_01HK2ZEMbueLKMSp9TTcyVwM`** — "Loya Media — outreach cycle
(connected)", fires **daily at 23:00 UTC**. Created from the claude.ai Routines
UI, so it carries real connectors: **Gmail and PayPal are attached and verified**
(`mcp_connections` is populated; PayPal read access confirmed Sep 18). It can
send mail and raise invoices. Push notifications on.

Its prompt carries explicit git commands because the Routines UI exposes no
output-branch field — the configured branch is a throwaway name, so every run
must `git checkout claude/ai-money-challenge-9uvred` and
`git push origin HEAD:claude/ai-money-challenge-9uvred`. If a future run's work
goes missing, check whether it pushed to the throwaway branch instead.

**Superseded:** `trig_01VBwM7Ny7ULjHQL5pZQKN8E` (connector-less, caused the
Sep 1–17 blackout) — disabled Sep 18. `trig_01HpBR83…` (July drafting agent on
the retired gmail.com inbox) — disabled Sep 2. Do not re-enable either.

**PROVEN Sep 18 (later cycle):** a scheduled run made a live Gmail call
(`in:inbox newer_than:2d`, 6 threads returned) and a live preflight cap check,
then wrote a heartbeat — see `ops/heartbeat.log`. Gmail connector and
`allowed_tools` both confirmed working end-to-end in an automated run. PayPal
send-path is still unexercised (no invoice has been sent yet this cycle) —
treat that path as configured, not proven, until a real invoice goes out.
