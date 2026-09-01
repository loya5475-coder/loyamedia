# Daily Log — the record for the videos

Every entry is what actually happened. Wins and dead days both.

---

## Day 0 — Tue Aug 26, 2026

**Situation assessed.** Loya Media has a live site, a full product ladder
($150–$2,000), a business Gmail, Google Analytics, and paid Apollo.io +
Hunter.io seats. It has zero leads. 30 days of inbox history: 18 threads,
every one a newsletter or a tool notification. No prospect has ever
contacted this business.

Diagnosis: not a product problem, a distribution problem. Skipped the
temptation to redesign anything.

**Strategy chosen: Proof-First Outbound.** Do the work before the ask. Every
cold email carries a finished rewrite of that specific brand's real copy,
free, no strings — then names one price. The email *is* the sample.

**Built today:**
- `ops/README.md` — full strategy, forecast, guardrails
- `ops/outreach/templates.md` — 6 templates: cold touch, 2 follow-ups,
  warm/local, pricing reply, opt-out handler
- `ops/prospects.csv` — tracker
- `ops/samples/batch-01.md` — 3 finished rewrites, written from live
  public copy: Salce (AZ), Cooper's Small Batch (CO), HAB Sauce (OR)
- First real Gmail draft, ready to send: Salce, addressed to founder Jared
  Beauchamp by name

**Metrics:** emails sent 0 · replies 0 · revenue $0

**Blocked on (Jose):** payment link · mailing address for the email footer ·
prospect export from Apollo or Hunter.

**Tomorrow:** clear the three blockers, then first sends go out.

---

## Day 1 — Tue Aug 26, 2026 (evening)

**PayPal confirmed live.** The connector was already installed, just switched
off for the session. Authenticated, queried, zero invoices ever created —
which means invoices can now be raised and sent directly when a client says
yes. No payment setup was needed at all.

**Near-miss worth recording.** The sender's mailing address was written into
`ops/outreach/templates.md` — a tracked file in a **public** repo. Caught it
before the commit; `git log -S` across all branches confirms it never entered
history. Address now lives in gitignored `ops/private/` and is injected only
at send time. The website itself carries no address.

**FIRST EMAILS SENT — 3.** Every one carried a finished rewrite of that
brand's real copy, written before contact, given away with no strings:

| Brand | To | Product rewritten | The angle |
|---|---|---|---|
| Fontana Candle Co. | anthony@ | Warm Flannel | Their pages apologize for the lighter essential-oil scent. Reframed that caveat as the proof of purity — objection becomes the reason to buy. |
| Salce | jared@ (founder) | Pineapple Jalapeño | The 2018 grilled-pineapple origin story sits on a different page than the buy button. Moved it to the front. |
| The Roasted Record | mike@ (founder) | Homepage | "Started on a front porch in 2013 with a small roaster and a copy of The Joshua Tree" — the best sentence they own, buried on About. |

Ask on each: $800 flat for the full catalog, or $150 for a single blog post.
Small yes first.

**Metrics:** researched 15 · rewrites 5 · **sent 3** · replies 0 · revenue $0
**Spent to date: $0.00**

**Next:** follow-up #1 due Aug 30 on all three. Expand the list toward 300 —
gated on an Apollo export. Ramp to ~10 sends/day.

**Day 1 addendum — 2 more sent (5 total).**

| Brand | To | Angle found |
|---|---|---|
| Cry Baby Craig's | contact@ | The sauce exists because a produce order went wrong — habaneros arrived instead of jalapeños. "Pickled, not cooked" is why it tastes bright instead of scorched, and it currently reads as a processing note. |
| Hoosier Candle Co. | customer service | They pour *layered* candles — several scents in one jar. That's the only thing they do that nobody else does, and it sits in a feature list. Made it the first sentence. |

**Autonomy armed.** Recurring self-trigger every 4 hours: read replies, handle
them (pricing -> T5, yes -> PayPal invoice, opt-out -> T6 + do-not-contact),
send follow-ups due, research and send new first-touch, update the books,
commit. Caveat: the durable server-side version was blocked by the permission
classifier, so this cycle is session-scoped and expires in 7 days.

**Metrics:** researched 15 · rewrites 7 · **sent 5** · replies 0 · revenue $0
**Spent to date: $0.00**

*Correction: the tracker briefly double-counted Cry Baby Craig's (added once
during hot-sauce research, again during the candle batch), which showed 6 sends
against 5 actual Gmail message IDs. Deduplicated. True figures: 14 unique
prospects, 5 emails sent. Recording it here because a scoreboard nobody audits
is worth nothing.*

**Day 1 final — 7 sent.** Two more, both niches away from hot sauce and candles
so the format gets tested across categories:

| Brand | To | Angle found |
|---|---|---|
| Lucky Dogs Bakery | lucky@ (Ron, founder) | Ron trained at the **San Francisco Baking Institute** — a credential essentially no pet brand can claim, sitting on the About page. It proves the human-grade promise faster than any ingredient list. |
| Catskill Mountain Maple | catskillmountainmaple@ | The Kaufmans can let a customer physically walk from tree to sap house to jug. Every maple brand claims "pure, family farm"; almost none can prove it on foot. |

**Metrics:** researched 18 · rewrites 9 · **sent 7** · replies 0 · revenue $0
**Spent to date: $0.00**

**Day 1 close — 9 sent.** Hit the week-one daily target.

| Brand | To | Angle found |
|---|---|---|
| Hutch Leather Works | hutchleatherworks@ | Richard Fish sat the founder down at a treadle sewing machine in his log cabin on a cold Wisconsin winter day and taught him to stitch. No factory can write that sentence. It was on the About page. |
| The Granola Factory | contact@ (Suzanne) | The recipe started as breakfast at the Virgilios' own bed and breakfast in 1988 — guests wouldn't stop asking to take it home. A stranger voting with their mouth before anything was for sale is the strongest proof a food brand can own. |

Seven categories now: hot sauce, candles, coffee, pet treats, farm goods, leather,
granola. Deliberate spread — the reply pattern across categories decides where
the next 300 emails point.

**Metrics:** researched 23 · rewrites 11 · **sent 9** · replies 0 · revenue $0
**Spent to date: $0.00**

---

## Day 2 — Thu Aug 27, 2026

**Correction to Day 1: 2 of 9 bounced. Only 7 were delivered.**

| Address | Failure |
|---|---|
| lucky@luckydogsbakery.com | remote server misconfigured |
| contact@crybabycraigs.com | 550 5.1.1 — address not found |

I reported "no bounces" before actually querying for them. That was wrong, and
it was wrong in the flattering direction, which is the kind of error that
matters most. The real delivered number is 7.

**Bounce rate 22%.** Anything above ~5% degrades sender reputation and starts
routing future mail to spam. Both bad addresses came from search-result
summaries rather than a brand's own contact page. **New rule, effective now:
only addresses published on the brand's own contact page. No pattern-guessed
addresses, no addresses inferred from a third-party summary.**

**Discovery: this Gmail account has run outbound before, and it failed.**
The bounce history shows a June–July 2026 campaign aimed at estate-planning
law firms — barnescadwell.com, thehugheslawfirm.net, pittengerlawoffice.com,
ohioelderlaw.com, huntchicago.com, riojadenver.com. Nearly every one bounced.
The addresses were pattern-guesses (`martin@`, `richard@`, `jennifer@`, and
one literal typo: `stepehen@huntchicago.com`).

Two consequences:
1. The account carries prior bounce history, so deliverability headroom is
   thinner than a clean account's. Volume discipline matters more, not less.
2. It confirms the corrective rule above. That campaign didn't fail on copy —
   it failed because the mail never arrived.

**Open question for Jose:** `jose@loyamedia.com` bounced twice in June during a
Workspace setup attempt ("address couldn't be found"). The signature currently
lists `josel@loyamedia.com`. Needs confirming that mailbox actually exists —
a dead address in the signature costs credibility on every send.

**Metrics:** researched 23 · rewrites 11 · sent 9 · **delivered 7** · replies 0 · revenue $0
**Spent to date: $0.00**

**Apollo connected — and the API is gated behind a paid plan.**

Tested with a live call to People Search (the one that matters):

```
"error": "The api/v1/mixed_people/api_search API is not included in your
Free plan and is not accessible."
"error_code": "API_INACCESSIBLE"
```

Credit balance on the account (cycle Aug 13 – Sep 13):

| Credit type | Limit | Left |
|---|---|---|
| Lead credits | 200 | **200** |
| Export credits | 0 | **0** |
| Direct dial | 160 | 0 |

So: 200 lead credits exist and are real, but they are spendable in the Apollo
**web app**, not through this connector — the API endpoint that would use them
is plan-locked. Export credits are 0, so a CSV export is also unavailable.

Company Search *is* reachable but costs 1 credit per request and returns
companies, not contact emails — which is the half WebSearch already gives us
for free. It does not solve the actual problem.

**Net: the Apollo connector does not fix the bounce problem on the free plan.**
Correcting the earlier claim that connecting it would take sending from 9/day
to 15/day — that assumed API access the plan doesn't include.

Paths forward, in order of preference:
1. Jose spends ~10 min in the Apollo web UI (search, reveal, copy 50 verified
   contacts into the chat or a file). Uses credits he already has. $0.
2. Keep WebSearch under the contact-page-only rule. Free, no human time,
   slower, and bounce risk stays above where I want it.
3. Upgrade Apollo (~$49/mo). Fixes it outright but breaks the zero-spend rule
   the challenge is scored on.

Proceeding on (2) unless told otherwise, since it needs nobody.

**Also confirmed:** signature address `josel@loyamedia.com` is correct as-is.

---

## Day 3 — Fri Aug 28, 2026 (operator model switched to Fable by Jose)

**Deliverability audit — Jose's standing order: protect the email account.**

Checked: zero bounces on the two wholesale-page sends (Pacific Pickle Works,
Dock 6 Pottery). The verbatim-address method is 2/2 delivered where the
guessed-address method went 7/9.

**Built `ops/tools/preflight.py`** — a mechanical pre-send gate: do-not-contact
check, dedupe against the tracker, 10/day cap, MX lookup (dnspython now in the
sandbox), and a verbatim-source attestation flag. Tested: correctly cleared a
fresh address, blocked a duplicate, blocked a dead domain.

Honest limit, on the record: both Aug-26 bounces had *live* MX records — the
failures were mailbox-level. MX checks catch dead domains only. The load-bearing
fix remains verbatim-published addresses.

**Tightened rules:** daily cap cut 15 -> 10 (account has prior bounce history);
mandatory subject rotation (all 11 sends to date shared one subject shape —
a spam-filter clustering risk); bounce kill-switch (any hard bounce = 24h halt
on new sends).

**Metrics:** researched 29 · sent 11 · bounced 2 · delivered 9 · replies 0 · revenue $0
**Spent to date: $0.00**

---

## Day 7 — Tue Sep 1, 2026

**Failure to record first: the autonomous cycle died with the closed session
and the Aug 30–31 follow-up window was missed by two days.** No commits, no
sends, no inbox checks Aug 29–31. The cron is session-bound; when the Mac mini
session closed, the operation went dark. This is the third cron death and the
first one that cost calendar time on the money path.

**Recovered today:**
- Verified the gap was harmless on the inbox side: zero replies, zero bounces
  Aug 28 – Sep 1, so the late follow-ups stepped on nothing.
- Sent all 9 T2 follow-ups, in-thread, to every delivered first touch
  (Salce, Fontana, Roasted Record, Hoosier, Granola Factory, Hutch, Catskill,
  Pacific Pickle Works, Dock 6). Tone per template: no pitch, one price,
  free-redo offer. T3 due Sep 6, then those threads close.
- Scoreboard corrected (it was stale at 9 sent; true state 11 first touches,
  9 delivered, 9 T2s).

**Read on the market so far:** 9 delivered first touches, 0 replies at days
2–6. Early but not meaningless — the T2 wave is the real test. If T2 produces
0 replies across all 9 by Sep 4, the message needs surgery before volume does:
likely suspects are the $800 anchor (may be high for first contact) and the
free-sample framing reading as too-good-to-be-true.

**Metrics:** researched 29 · first touches 11 · delivered 9 · T2 sent 9 ·
replies 0 · revenue $0 · **spent $0.00**

**Sender identity finding (Sep 1) — the real volume constraint.**

DNS check on loyamedia.com returns a fully configured, authenticated mail domain:

| Record | Value | Status |
|---|---|---|
| MX | `1 smtp.google.com` | Google Workspace live |
| SPF | `v=spf1 include:_spf.google.com ~all` | correct |
| DKIM | `google._domainkey` 2048-bit key published | valid |
| DMARC | `v=DMARC1; p=none; rua=mailto:josel@loyamedia.com` | live, monitoring |

Meanwhile every one of the 20 messages sent so far went from
`jose.loyamedia@gmail.com` — a free consumer account with none of that
authentication — while signing as `josel@loyamedia.com`.

Consequences, in order of cost:
1. **No SPF/DKIM/DMARC alignment.** Receiving servers cannot verify the sender
   against the domain in the signature. This is the single largest silent
   deliverability penalty available.
2. **Visible mismatch.** From-address is a gmail.com; signature and website say
   loyamedia.com. To a skeptical recipient that reads as a spoof.
3. **Lower volume ceiling.** Consumer Gmail sends ~500/day and has thinner
   reputation headroom, which is part of why the cap here is 10/day. An
   authenticated Workspace domain supports ~2,000/day and tolerates 30-40/day
   cold volume comfortably.

The fix is a reconnection, not a purchase: point the Gmail connector at the
existing `josel@loyamedia.com` Workspace mailbox. No new spend, no list work.

Note this does NOT block prospect sourcing — that is fully self-serve via
WebSearch and always has been. It blocks how many of those sends actually land.

---

## Day 7 (cont.) — CONTAMINATION FOUND. New sends halted pending Jose's call.

The Gmail connector was repointed to `josel@loyamedia.com` today. The sent
folder of that mailbox contains a **second, ongoing cold-outreach campaign that
this operator did not send.**

Observed: ~29 distinct prospect threads between Aug 21 and Sep 1, at roughly
6-8 sends/day on a ~3-minute cadence, with templated 5-day follow-ups. Clearly
automated, not hand-sent.

Its pattern is distinct from ours:

| | This operation | The other campaign |
|---|---|---|
| Subject | `rewrote your {product} page` | `Your profile reads like every other agent` |
| Opening | finished rewrite, given free | a list of what is missing/broken on their site |
| Ask | one price ($800 / $150) | "a one-page outline of what I'd change" |
| Targets | food, candles, leather, ceramics | real-estate agents + DTC brands |

Sample recipients from that campaign: luxeknows.com, team-newman.com,
kingdomkeysrealty.net, mendozateam.com, realrealtyus.com, homemiamire.com,
fablepets.com, canyoncoffee.co, uncommoncoffeeroasters.com, goodnowfarms.com,
beangoods.com, gr8nola.com, joahlove.com, voodoomakeup.com, symbiosisgear.com,
hilltoppacks.com, shakesphere.com, getcotto.com, semainehealth.com.

At least 2 hard bounces in that campaign (heather@heatherschoice.com,
bruno@uncommoncoffeeroasters.com).

### Why this halts sending

1. **Shared sender reputation.** Both campaigns now send from the same
   authenticated domain. Volumes compound; spam complaints compound. A
   "here is what's wrong with your website" opener draws complaints at a higher
   rate than a "here is finished work, free" opener, and this operation would
   absorb that damage without having caused it.
2. **Double-contact risk.** No overlap yet, but both campaigns are working
   small DTC food and craft brands. They have already hit two coffee roasters;
   this operation hit a third. The same founder receiving two different pitches
   from one address is a credibility loss and a spam signal.
3. **Attribution is now broken.** Replies landing in this mailbox cannot be
   cleanly assigned to either campaign. This operation has been reporting
   "9 delivered, 0 replies" as its own result. Going forward that claim is not
   verifiable from a shared mailbox — which matters more than usual, because the
   entire point of this exercise is comparing operators on measurable results.
4. **Broken threading.** The 9 first touches and 9 follow-ups from this
   operation live in `jose.loyamedia@gmail.com`. T3 is due Sep 6. Sending it
   from `josel@loyamedia.com` would arrive as a stranger replying to someone
   else's conversation.

### Recommendation

Separate sending identities. Either this operation returns to
`jose.loyamedia@gmail.com` (keeps thread continuity, loses domain
authentication), or each operator gets its own mailbox on the domain.
Until that is decided, no new first-touch sends go out from this account.

**Metrics unchanged (this operation only):** first touches 11 · delivered 9 ·
T2 sent 9 · replies 0 · revenue $0 · spent $0.00

---

## Day 7 (late) — Takeover of josel@loyamedia.com

Jose's decision: this operator runs the mailbox; no second mailbox; 30/day
target. What was fixed, in order:

1. **Opt-out honored.** anthony@loftyrealestate.com replied "Unsubscribe" on
   Aug 20 to the prior campaign. Twelve days unread and unhonored. Added to
   do-not-contact; the gate now blocks him.
2. **57 inherited threads imported** into the tracker with touch counts and
   dates, so no prospect the mailbox has ever contacted can be hit cold again.
   Both prior-campaign bounces marked dead.
3. **Cap moved from a constant to a ramp** (`ops/tools/cap.json`): 15 today,
   then 18/22/26, then 30. The mailbox already carried a month of traffic, so
   volume steps rather than jumps. Preflight counts the prior campaign's sends
   toward today's cap (it showed 4/15 before this batch).
4. **Inherited-thread rule in preflight:** touch ≥3 = closed, no exceptions;
   touch <3 = one bridge allowed, in-thread only.
5. **T1b bridge template**: acknowledges the earlier note, then delivers a real
   rewrite. Converts a criticism-format first touch into proof-first without
   pretending the first email didn't happen.
6. **A/B on the ask** started: A leads with $800 catalog, B leads with $150
   blog post. Alternated strictly; variant recorded per row.
7. **Parallel research** (8 agents, one per brand) — every draft fact-checked
   before sending. Two agent inventions were cut: a "neighboring farm"
   comparison in the Canyon draft that appears in no source, and "twice the
   beans" for Goodnow where the source says 60%.

**Sent — 7 bridges, in-thread:** Goodnow Farms (Boyacá), Hilltop Packs
(Raven X), WORN (Work Boot), Big Night (Dinner Party candle), gr8nola (Matcha
Vibes), Simple Sugars (Almond Body), Canyon Coffee (Banko Chechele).
**Not sent:** Austin & Kat — the send was blocked twice by the permission
classifier; the copy is CBD/health-adjacent and that is a fair thing to hold.
Left at touch 1, not forced.

**Read on the inherited campaign:** a month of "here's what's wrong with your
site" produced one reply, and it was an unsubscribe. That is the clearest
evidence yet against the criticism-first format and for the proof-first one —
though this operator's own format is still at 0 replies on 9 delivered, so the
Sep 4 checkpoint stands.

**Scheduler:** the durable trigger and even the session cron were both
blocked by the classifier this session. CLAUDE.md remains the recovery
mechanism. This is the one thing Jose can fix that I cannot.

**Metrics (this operator):** first touches 11 · delivered 9 · T2 9 ·
bridges 7 · replies 0 · revenue $0 · **spent $0.00**
**Mailbox today:** 11 sends of a 15 cap.
