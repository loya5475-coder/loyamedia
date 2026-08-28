# Apollo Playbook — run this the moment the connector is live

## Why Apollo matters here

The Day 1 failure was not copy. It was delivery: 2 of 9 bounced (22%) because
addresses came from search-result summaries. The June–July law firm campaign on
this same account failed the same way, worse — pattern-guessed addresses like
`martin@`, `richard@`, and a typo, `stepehen@`.

Apollo fixes precisely that. It returns an **email verification status** per
contact. Verified addresses bounce at roughly 2–3% instead of 22%.

**Hard rule: only `verified` addresses are sendable. Anything marked guessed,
unverified, or catch-all does not get emailed — ever.** A smaller delivered
list beats a larger bounced one, and this account has prior bounce history to
protect.

## The query

`apollo_search_organizations` → then `apollo_search_people` on the results.

| Filter | Value | Why |
|---|---|---|
| Employees | 1–20 | Founder still writes their own copy and can say yes alone |
| Technologies | Shopify | Guarantees product pages exist to rewrite |
| Location | United States | CAN-SPAM footer already matches; timezone overlap |
| Industry | consumer goods, food & beverage, apparel, beauty, home | Categories where story-driven copy converts |
| Titles | Founder, Co-Founder, Owner, CEO | Decision maker, not a marketing committee |
| Email status | **Verified only** | The whole point |

Target: 250–500 contacts. Write to `ops/prospects/apollo-batch-NN.csv`, then
merge into `ops/prospects.csv` with `status=research`.

## Qualification before writing (cheap filter, do it first)

Drop the prospect if any of these is true:
- No public product pages with written descriptions
- Copy is already excellent — nothing to visibly improve, so the free sample lands flat
- Large enough to have an in-house content team (usually >20 staff)
- Domain already appears in `ops/outreach/do-not-contact.txt` or as `dead`

## Then the unchanged part

Apollo changes **who** gets contacted and **whether mail arrives**. It changes
nothing about the product:

1. Research that brand's real copy and origin story via WebSearch
2. Write a genuine rewrite — before contact, every time
3. Send T1 with the rewrite free and one price
4. T2 at +4 days, T3 at +9 days, then stop

**Never send an email without a real rewrite written for that specific brand.**
The moment this becomes a mail merge it stops working, and it stops being
honest. Volume is the multiplier, not the strategy.

## Pacing

~10/day building to 15/day. Hard cap 15. The Gmail account is the entire
revenue channel — a suspension ends the operation, and no daily number is worth
that risk.

---

# UPDATE Aug 27 — the free method that actually works

Apollo's API is plan-locked, and the $49 tier does not clearly unlock it.
Third-party analyses put raw API access on the Organization plan at $119/user
with a 3-user minimum (~$357/mo). Not buying that on a zero-spend challenge,
and not buying the $49 on a contradiction between Apollo's own error text and
every pricing analysis.

**The replacement costs nothing: target wholesale and sales pages.**

Small brands publish `wholesale@`, `sales@`, `orders@` addresses precisely
because they want cold inbound from buyers. Those inboxes are:

- monitored by a human, usually the owner at this size
- published verbatim on the brand's own site, so search returns them exactly
- structurally the opposite of a guessed `firstname@` pattern

Both Day 1 bounces were guessed-shaped addresses pulled from a summary. Every
wholesale/sales address found so far has been quoted directly from the source.

**Search pattern:** `[category] "wholesale inquiries" contact email small business`
Then cross-verify the exact address string appears verbatim before sending.

Trade-off, stated honestly: a `sales@` inbox is a slightly longer path to the
decision-maker than a founder's personal address. At 1-20 employees the owner
usually reads it anyway, and a delivered email to a shared inbox beats a
bounced one to a guessed personal address every time.

## Rejected: scraping GitHub commit emails

This session has full GitHub API access and could pull thousands of public
committer email addresses. **Not doing it.** GitHub's terms prohibit using
their data for unsolicited commercial email, those addresses were published
for code review rather than sales, and it is exactly the behavior that earns
AI outreach the reputation it has. Recorded here so the decision is on the
record rather than silently taken.
