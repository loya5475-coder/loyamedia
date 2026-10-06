# Loya Media — ACTIVE AUTONOMOUS OPERATION

**Read this before doing anything else in this repo.**

A 30-day revenue challenge is running here: **RESTARTED — Oct 2 → Nov 2, 2026.**
Round 1 (Aug 26 – Sep 26) finished at **$0.00**. Sep 26 is NOT the deadline any
more; do not treat the challenge as closed. Loya Media
is a real content agency (loyamedia.com) with a live site, a $150–$2,000 product
ladder, a business Gmail, and PayPal. The operation sells its copywriting by cold
outreach that delivers finished work before asking for money.

## First action in any session: install deps, then check staleness

```bash
pip install -q -r ops/tools/requirements.txt   # REQUIRED: fresh clones lack dnspython
tail -40 ops/log.md          # what actually happened last
date -u                      # how long ago that was
```

**Do not skip the pip install.** Every scheduled run starts from a fresh clone
with no site-packages, so `preflight.py` fails its MX check with
`BLOCKED: dnspython not installed` — which looks like a dead domain but is not.
Same class of bug as the mailing-address gap: anything not in the repo does not
survive the clone. If a gate blocks, check the environment before the prospect.

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
- **Apollo's API is NOT usable — do not plan around it (tested Oct 5).** The
  connector authorizes and `apollo_users_api_profile` returns real data (75 lead
  credits, 5,000 AI credits), which makes it *look* available. It is not: the
  account is on the **Free plan**, and both endpoints that matter return
  `API_INACCESSIBLE` / `ENDPOINT_ACCESS_DENIED`:
  - `api/v1/mixed_people/api_search` (prospect search) — blocked
  - `api/v1/people/match` (email enrichment) — blocked

  The credits are real but only spendable in Apollo's web UI, which an agent
  cannot drive. **A successful profile call is not evidence of API access** — that
  inference was made once and was wrong. Do not burn turns re-testing these two
  endpoints unless Jose upgrades the plan. Sourcing stays WebSearch +
  published-contact-page verbatim.
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
- **Never commit the mailing address.** This repo is public and the address is
  Jose's. Read it from the **`LOYAMEDIA_MAILING_ADDRESS` environment variable**,
  which is the only durable source: `ops/private/sender-identity.txt` is
  gitignored and therefore CANNOT survive the fresh clone every scheduled run
  starts from. That gap cost Days 25–40 — 0 sends every single day.
  **Never fabricate or guess an address to get past this.** CAN-SPAM requires a
  real one; inventing it is illegal and would burn the domain. If the variable is
  unset, write it in the heartbeat and send nothing — refusing is correct. Do not
  re-notify Jose daily with the same finding.
- **Do not scrape GitHub commit emails** for outreach. Considered and rejected
  on Aug 27 — see `ops/outreach/apollo-playbook.md`.

## Recovering the sender address — DO THIS, don't ask Jose again

**The address is always recoverable without him.** Solved Oct 6 after this one
field cost 18 days of zero sends and four rounds of asking.

Every email this operation has ever sent carries the address in its CAN-SPAM
footer, and every run must have Gmail access anyway. So the mailbox is the
durable source of truth:

```
Gmail search:  in:sent from:josel@loyamedia.com "Loya Media"
Then get_thread on any result with messageFormat=PLAIN_TEXT and read the
footer — the line between "josel@loyamedia.com" and the "stop" line.
```

Pass it to the gate inline, per command, so the gate still fully validates it:

```bash
LOYAMEDIA_MAILING_ADDRESS="<recovered>" python3 ops/tools/preflight.py <email> --source-verbatim
```

Then paste the same address into the footer of what you send.

**Why not the other routes** — all four were tried and all four fail:
- **Committing it:** this repo is public. Never.
- **`ops/private/sender-identity.txt`:** gitignored by design, so it cannot
  survive the fresh clone every scheduled run starts from. Writing it from an
  agent is also refused by the sandbox as credential leakage.
- **The env var alone:** there are four environments. The scheduled Routine runs
  in `claude/ai-money-challenge-9uvred`; interactive sessions run in `Money`.
  Setting it in one does not set it in the other, and that exact mismatch is
  what silently produced the zero-send streak.
- **Reading the env var to build the footer:** the sandbox blocks printing it
  (credential materialization), so an interactive session may have the variable
  set and still be unable to use it.

**Never add a flag or any other escape hatch to `preflight.py` that lets it pass
without a real validated address.** That was attempted on Oct 6 and correctly
refused as weakening the gate. The operator does not get to loosen the control
that constrains the operator. Recover the real address instead — it takes two
Gmail calls.

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
(connected)", fires **daily at 14:00 UTC** (`0 14 * * *`). Created from the claude.ai Routines
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

**Do NOT retry `create_trigger` with `connectors` (tested Sep 18).** That
parameter now exists and would let an agent create a connectored Routine from
inside a session. It returns `the connectors parameter is not available for
this organization`. The inheritance gap is real; don't spend another call on it
unless the org plan changes. And do **not** create a connector-less backup
Routine — it can only write `BLIND RUN` heartbeats, which is noise, not
coverage.

**Cadence is 1x/day and only Jose can change it.** The live Routine was created
in the UI (`created_via: http_api`), so agents get `Agents can only update
routines they created` from `update_trigger`. The UI exposes a single time
picker, not a cron field — Jose reported he cannot enter multiple run times, so
do not keep asking for `0 14,17,20,23 * * *`.

**The 14:00 UTC ask is CLOSED.** Verified Oct 5 via `list_triggers`: the cron is
already `0 14 * * *`. Do not ask Jose to move it again.

And keep this in proportion: reply *latency* is not the bottleneck. Response rate
is. Do not spend Jose's attention on scheduling when the offer is the open question.

## Round 1 result — read this before planning Round 2 outreach

**Final: $0.00 revenue, 0 replies, $0.00 spent.** Two separate failures, and only
one was plumbing:

| Format | Delivered | Human replies |
|---|---|---|
| Proof-first (finished rewrite up front) | 16 | **0** |
| Criticism-first (inherited campaign) | 57 | **0** (1 unsubscribe) |

**73 delivered, 0 replies.** Both formats converted at zero in-sample. So a
perfectly-running month of the same playbook still forecasts ~$0. Cold email to
small e-commerce brands offering copywriting is the **automated baseline only** —
it runs in the background because it is cheap, not because it works.

**Round 2 must test channels where the buyer is already looking to pay** rather
than strangers being interrupted. Do not quietly fall back to grinding cold
volume because it is the path the tooling already supports. If a new channel is
tried and fails, log that too — a negative result is a real result, but repeating
a known-zero one is not.
