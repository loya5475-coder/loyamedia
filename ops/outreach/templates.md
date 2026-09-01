# Outreach Templates

Rules that override everything below:
- The rewrite is written **before** the email. If there's no real rewrite, there's no send.
- One ask per email. One price. No menu.
- Under 150 words above the signature. The rewrite is the length; the pitch is not.
- Never claim clients, results, or testimonials we don't have.
- Signature block is fixed and includes a real address + working opt-out.

---

## T1 — Cold, first touch ("Already Done")

**Subject:** rewrote your {{product_name}} page
*(alternates: `{{product_name}} — a rewrite, free` · `your {{product_name}} description`)*

```
Hi {{first_name}},

I write product copy for small e-commerce brands. I rewrote your
{{product_name}} description as a sample. No charge, no catch — it's
yours whether or not we ever speak.

---
{{rewrite}}
---

The change: {{one_specific_reason}}

If you want the rest of the catalog in that voice, it's $800 flat for up
to 30 products, delivered in about a week. If you'd rather start smaller,
a single SEO blog post is $150.

Either way, the copy above is yours — paste it in today.

{{signature}}
```

`one_specific_reason` must name an actual craft decision, e.g.
- "yours opens with the wax type; buyers decide on the feeling first and check specs second."
- "there was no reason to buy today. That last line gives one without discounting."
- "it now reads in your voice from the About page instead of generic DTC-speak."

---

## T2 — Follow-up #1 (day +4)

**Subject:** *(reply in thread — no new subject)*

```
Hi {{first_name}} — did the {{product_name}} rewrite land okay?

No pitch attached. If it's useful and you want the other {{n}} products
done the same way, that's the $800 flat. If it's not the direction you'd
want, tell me why and I'll redo it once, free — I'd genuinely like to know
where I read your brand wrong.

{{signature}}
```

---

## T3 — Follow-up #2 (day +9, final)

**Subject:** *(reply in thread)*

```
{{first_name}} — last one from me, I won't keep knocking.

If copy isn't the priority this quarter, that's a completely fine answer.
If it is but $800 is the wrong size, the smallest useful thing I do is a
single blog post at $150 — researched, SEO-ready, published-ready.

Otherwise I'll leave you to it. The rewrite stays yours.

{{signature}}
```

Nothing after T3. Three touches, then the prospect is closed as `no-response`
and never re-contacted this cycle.

---

## T4 — Warm / local first touch

**Subject:** {{business_name}} — wrote you something

```
Hi {{first_name}},

{{how_we_know_them}}. I started a content-writing shop — Loya Media —
and I've been rewriting copy for small businesses.

I did three pieces of yours already, attached below. Free, no strings,
I just wanted you to see the quality rather than read me describe it.

---
{{rewrites}}
---

If it's useful, my smallest package is $150 and the full store rewrite is
$800. If it's not, keep the copy anyway and tell anyone you think it'd help.

{{signature}}
```

---

## T5 — Reply handler: "how much / what's the catch"

```
No catch — the free rewrite is how I'd rather introduce myself than with a
pitch deck.

Pricing, plainly:
· Single blog post — $150
· 30-day social caption pack — $350
· 5-email welcome sequence — $400
· Homepage + About page — $500
· Full store rewrite, up to 30 products — $800
· Monthly retainers from $500

No contracts, cancel any time. If you want to start, tell me which one and
I'll send an invoice and get going the same day.

{{signature}}
```

---

## T6 — Reply handler: "not interested / stop"

```
Understood — I won't email you again. The rewrite's still yours to use.

Best of luck with {{business_name}}.
```
Then add to `ops/outreach/do-not-contact.txt` immediately.

---

## Signature block (fixed, every email)

```
— Jose Loya
Loya Media · content that converts
loyamedia.com · josel@loyamedia.com

{{physical_address}}   <-- pulled at send time from ops/private/sender-identity.txt (gitignored)
Don't want to hear from me again? Just reply "stop" and you won't.
```

`physical_address` is REQUIRED before any cold send. Commercial email without
a valid physical postal address violates CAN-SPAM.

---

## Deliverability rules (added Aug 28 — mandatory)

1. **Preflight every send:** `python3 ops/tools/preflight.py <email> --source-verbatim`
   must print CLEAR. No exceptions, including follow-ups to new addresses.
2. **Rotate subjects.** Never two consecutive sends with the same subject shape.
   Rotation pool:
   - `rewrote your {product} page`
   - `your {product} description — a rewrite, free`
   - `wrote this for {brand}`
   - `{brand}'s {product} page, rewritten`
   - `a free rewrite of your {product} copy`
3. **Bounce kill-switch.** Check mailer-daemon 30–60 min after each batch.
   ANY hard bounce -> stop new sends for 24h, mark prospect dead, log it,
   re-verify sourcing method before resuming. Follow-ups to already-delivered
   threads may continue (those addresses are proven).
4. **Cap 10/day** (was 15). This account carries prior bounce history from the
   June–July campaign; headroom is thinner. Spread sends across the day —
   no bursts of 5+ in one hour.
5. **Warm signal:** any reply, even a "no", is a deliverability asset. Always
   respond politely and promptly — replies tell Gmail this is wanted mail.

---

## T1b — Bridge (for INHERITED threads only, sent in-thread as a reply)

Use when the prospect already received a criticism-format first touch from this
mailbox under the prior operator. Converts a weak first touch into the
proof-first format without pretending the earlier email didn't happen.

**Subject:** *(reply in thread)*

```
Hi {{first_name}} — following up on my note from last week. Rather than tell
you what I'd change, I went ahead and rewrote your {{product}} page. No charge,
no catch — it's yours whether or not we ever speak.

---
{{rewrite}}
---

The change: {{one_specific_reason}}

{{ask_variant}}

Either way, the copy above is yours.

{{signature}}
```

## Ask variants (A/B, alternate strictly; record in tracker)

**A — catalog first**
```
If you want the rest of the catalog in that voice, it's $800 flat for up to 30
products, delivered in about a week. If you'd rather start smaller, a single
SEO blog post is $150.
```
**B — blog post first**
```
If it's useful, the smallest thing I do is a single SEO blog post at $150 —
researched, ready to publish. The full catalog rewrite is $800 flat for up to
30 products if you want everything in that voice.
```

## Sender identity (from Sep 1, 2026)
All mail goes from `josel@loyamedia.com` (Workspace, SPF/DKIM/DMARC aligned).
The 9 threads started from jose.loyamedia@gmail.com get their final touch as a
fresh message from josel@ with "Re: <original subject>" for continuity.
