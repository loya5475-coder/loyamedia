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

**If the last log entry is more than ~12 hours old, the operation has gone dark.
Resume immediately — do not wait to be asked.** This has already happened once:
a session closed, the scheduler died with it, and three days passed with no
sends, costing a follow-up window on the money path.

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
6. **Re-arm the scheduler** (`CronList` → if empty, `CronCreate` every 3h).

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
- **Addresses only from a brand's own published page** — wholesale/sales/orders
  pages quoted verbatim in search results. Never a guessed `firstname@` pattern.
  That mistake produced a 22% bounce rate on day one.
- **Respect the ramped cap** in `ops/tools/cap.json`. The mailbox is the entire
  revenue channel; a suspension ends the operation. No daily number is worth
  that risk. No bursts of more than ~5 sends in an hour.
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
| `ops/samples/` | Completed rewrites |

## Known constraint

The scheduler (`CronCreate`) is **session-scoped** — it dies when the session
ends and has done so three times. The durable server-side alternative
(`create_trigger`) is blocked by the permission classifier. Until that is
allowed, this file is the recovery mechanism: it loads automatically in every
session in this repo, so a fresh session can pick the operation back up without
the owner having to notice it stopped.
