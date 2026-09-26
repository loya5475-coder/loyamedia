# Scoreboard — Aug 26 → Sep 26, 2026 · updated Sep 26 (DEADLINE DAY CLOSE-OUT)

## STATUS: Declared 30-day window closes today at $0 revenue.
16 days lost to a connector-less trigger (Sep 1-17). A further 8 days
(Sep 19-26) lost to a missing physical-address file that a fresh container
clone cannot persist -- every other part of the pipeline (Gmail, bounce/reply
detection, research, rewrites, the send gate) worked the whole time. Net: 24
of 30 days unable to send, for two sequential, fixable, non-product reasons.
See ops/log.md Day 32 for the full accounting and the one remaining unblock
(a LOYAMEDIA_MAILING_ADDRESS env var Jose has not yet set).

| Metric | Actual | 30-day target |
|---|---|---|
| Emails sent (own, proof-first) | 11 first touch + 7 bridges = 18 | 300 |
| Delivered | 16 | 300 |
| **Human replies** | **0** | 25 |
| Paid clients | 0 | 3–4 |
| **Revenue collected** | **$0.00** | $1,500–$3,500 |
| Spent | $0.00 | $0 |

Last send: Sep 1. No sends, no follow-ups, no replies Sep 2–17.
Durable trigger fired 60× but ran connectorless (no Gmail/PayPal) — accomplished nothing.

## The two formats, head to head (the one real finding)
| Format | Delivered | Replies |
|---|---|---|
| Proof-first (finished rewrite, this operator) | 16 | 0 |
| Criticism-first (inherited campaign) | 57 | 0 real (1 unsubscribe) |

Neither converted in-sample. Numbers checkable against Gmail message IDs.
