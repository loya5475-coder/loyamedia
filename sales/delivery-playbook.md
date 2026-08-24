# Delivery & Handoff Playbook
### From "yes" to live website to $50/mo recurring — step by step

This is the exact sequence after a client says yes at the appointment. Total timeline: **5–7 days**. Tell them "one week" and deliver in five days — early delivery is the cheapest wow you'll ever buy.

---

## Step 0 — At the appointment, the moment they say yes

1. **Collect the deposit on the spot: $400 (50%).** Send a PayPal invoice from your phone (you already have the "Pay an invoice" flow on loyamedia.com) or take Zelle/Venmo — whatever they actually use. Trades guys often prefer Zelle. *A yes without money is a maybe.*
2. **Get the content while you're sitting there (10 minutes, one time — never chase them later):**
   - 10–15 job photos texted from their phone to yours
   - Their preferred phone number for the site + email for the quote form (if no email, form submissions can go to your email and you text them the lead — that's actually an upsell-worthy service)
   - Exact business name spelling, license number if they have one, hours, list of services, towns they work
   - Which domain they like: get 2–3 options ready ([businessname].com, [tradecity].com)
3. **Set the handoff meeting NOW:** "I'll have it live by [day]. Let's meet [day+1] same time so I hand it over and show you how it works." Two meetings scheduled = deal that doesn't ghost.
4. Text them a one-line receipt: *"Got it — $400 deposit received. [Business].com will be live by Friday. Balance of $400 + first month's $50 hosting due at handoff. — Jose, Loya Media."* That text is your paper trail. (For extra protection, a one-page agreement with scope + price + "client owns domain, Loya Media manages hosting" is worth having — a lawyer-free template is fine at this price point.)

## Step 1 — Buy the domain (Day 1, ~$10–12)

- Buy it in **Loya Media's registrar account** (Namecheap or Porkbun — Porkbun is usually cheapest, ~$10/yr for .com, WHOIS privacy free).
- One Loya Media account holding ALL client domains = one dashboard, one renewal list, and the reason your $50/mo is sticky (you manage everything; they never touch DNS).
- **Be straight with clients:** the domain is theirs — if they ever leave, you transfer it to them. Say this proudly at the pitch ("no contract, your domain, you keep it") — it closes deals AND keeps you honest. Holding domains hostage is how you get a bad reputation in a small market.
- Turn ON auto-renew. A client's expired domain is a fire you never want.

## Step 2 — Build the real site (Day 1–2)

1. You already have the demo from landingsite.ai (built before the cold call). Now upgrade it to final:
   - Swap stock/placeholder images for their real job photos
   - Correct every fact: services, hours, license #, towns, exact phone number
   - Paste in their real Google reviews (3–5 best)
   - Wire the quote form to the right email
2. Run the follow-up polish prompts from `landingsite-prompt-template.md`.
3. **Test on your own phone like a customer:** tap the call button (does it dial?), submit the quote form (does the email arrive?), scroll every section, check load speed.

## Step 3 — Connect the domain (Day 2–3)

1. In landingsite.ai: open the site's settings → **Custom Domain** → enter the domain.
2. It will show you DNS records (typically an A record and/or CNAME, e.g. `www` → their host). Copy them.
3. In Namecheap/Porkbun: domain → DNS settings → add exactly those records. Delete the registrar's default parking records.
4. Wait for propagation (usually 15 min – 2 hours; can be up to 24). Verify in landingsite.ai — it'll confirm and issue the SSL certificate automatically. **The site must show the padlock (https)** before you deliver — "Not Secure" in the browser bar kills trust instantly.

## Step 4 — Pre-launch checklist (Day 3–4)

- [ ] https padlock shows on the custom domain
- [ ] Click-to-call works from a real phone
- [ ] Quote form delivers (send a test lead, confirm receipt)
- [ ] Every phone number on the site is correct (call each one!)
- [ ] Business name spelled correctly EVERYWHERE (owners notice instantly)
- [ ] Looks right on: iPhone, Android, laptop
- [ ] Title tag reads "[Business] | [Trade] in [City], [ST]"
- [ ] Reviews section quotes real reviews
- [ ] Their Facebook page linked (if they have one)
- [ ] Google Search Console: add the domain, submit for indexing (10 min, free — this is how it starts showing on Google)

## Step 5 — The handoff meeting (Day 5–7)

This is a ceremony, not an email. Do it in person or on a call — never just text a link.

1. **Show it live on THEIR phone.** Google the domain together. Let them scroll. Let them tap the call button and feel their own phone ring.
2. Walk through: "Here's what customers see... here's what happens when they hit Get a Quote — it comes straight to you... here's your reviews selling for you 24/7."
3. **Link it everywhere while you're together (this is where the site starts working):**
   - Add the website to their **Google Business Profile** (they log in, you drive — 3 minutes, and it's the single biggest visibility win)
   - Add the link to their Facebook page, Instagram bio, Yelp listing
   - Tell them to put it on their truck, cards, and yard signs when they next reprint
4. **Collect the balance: $400 + set up hosting.** For the $50/mo, set up a **PayPal recurring subscription** (or Stripe payment link with monthly billing) right there on their phone — auto-charge, not "I'll pay you each month." Auto-billing is the difference between recurring revenue and a monthly chase.
5. Hand them a one-page "Your Website" sheet: the domain, what the $50/mo covers (hosting, security, SSL, edits within reason, you on text), and your number.
6. **Ask for two things before you leave:**
   - A Google review — for Loya Media, from them, right now, on their phone ("it takes 60 seconds and it's how I get found, just like your reviews get you found")
   - A referral: "Who do you know — a plumber, an electrician, a buddy with a crew — who needs this? I'll take care of them." Trades owners all know 10 other trades owners. **This is your best lead source from client #1 onward.**

## Step 6 — Aftercare (the part that keeps the $50/mo forever)

- **Day 30:** text them a screenshot of their site's Google ranking or visit count. "Your site came up #2 for 'stucco repair Las Cruces' this month." Thirty seconds of your time; renews the subscription emotionally.
- **Monthly:** one check that the site loads, SSL is valid, form works. (Set a calendar reminder; it's 2 minutes per client.)
- **Edits:** small text/photo swaps are included — do them same-day and say "done ✅". Same-day small edits are why nobody ever cancels.
- Bigger asks (new pages, rebrand) = quoted separately. "That one's a bigger job — I'll do it for $X."

---

## Managing the $50/mo subscriptions (recurring billing + cancellations)

### Set up recurring payments with Stripe (recommended)

1. Create a free account at stripe.com (no monthly fee; they take 2.9% + 30¢ per charge — so ~$1.75 of each $50).
2. Products → add **"Website Hosting & Care — $50/month"** as a recurring price.
3. Create a **Payment Link** for it. That gives you a URL (and a QR code) you can text to the client at handoff — they enter their card once on their phone, and Stripe auto-charges them every month forever. No invoicing, no chasing.
4. Install the **Stripe mobile app** — you get a push notification on every successful payment and every failure, and you can see all your subscribers in one list. That list IS your hosting business.
5. Alternative: PayPal Subscriptions works the same way if a client insists on PayPal (you already take PayPal). **Zelle/Venmo can't do auto-recurring** — fine for the $800 build, wrong for hosting; you'd be chasing 30 people by text every month.

**Failed cards (this is most "cancellations"):** Stripe automatically retries failed charges over ~2 weeks and emails the client to update their card. If it still fails, you text them personally: *"Hey [Name], your card on file expired — here's the link to update it so the site stays up."* Most churn is expired cards, not unhappy clients. Handle it warmly and fast.

### Cancellations: the notify-and-save flow

At your scale, a cancellation won't come through a portal — **it comes as a text to you**: "hey I want to cancel the website thing." That's actually better than any automated popup, because the save conversation is yours. (Stripe also lets clients cancel via its billing portal if you enable it — if you do, turn on **cancellation reasons** in portal settings and you'll see why they left in the dashboard, plus get the app notification. For now, keep cancellation manual: they have to contact you, which guarantees you get your second chance.)

**The save script — always ask WHY before you cancel anything:**

> "No problem at all — I'll take care of it. Before I shut it down, can I ask what's going on? Just want to make sure I didn't drop the ball somewhere."

Then match the real reason:

| They say | You offer |
|---|---|
| "Money's tight right now" | **Pause plan:** "Let's not kill the site — I'll drop you to $25/mo for the next 3 months, site stays live, we revisit in the fall." (A paused client at $25 beats a cancelled one at $0, and they almost always return to full price.) Or: "Prepay the year at $500 and save $100." |
| "I'm not getting calls from it" | "Fair — let me earn it. This week, free: I'll optimize your Google Business Profile and set up a review QR card for your crew. Give it 60 days; if it's still doing nothing, I'll cancel it myself and refund the last month." Then send them the visit/ranking screenshot monthly so they SEE the value. |
| "I'm retiring / closing the business" | Let them go graciously. Transfer the domain to them, thank them, ask for a Google review and one referral on the way out. |
| "My nephew's taking it over" | "Totally fine — the domain's yours, I'll transfer everything over. And if it ever gets to be a hassle, one text and I'll take it back on." Door stays open; half come back. |

**Rules for the save:**
- Keeping a client is 10× cheaper than cold-calling a new one. Always make ONE genuine save offer.
- Two offers max, then let go warmly. Begging costs you referrals in a small market; grace earns them.
- Log every cancellation reason (even in a notes app). Three people saying "not getting calls" means your Day-30 value texts aren't happening — fix the system, not the client.
- Never hold the site or domain hostage. Ever. Word travels fast between contractors — your reputation IS your pipeline.

## What the $50/month covers (say this list out loud when selling it)

> "Hosting, your domain renewal, security and the SSL certificate, keeping it fast, small changes whenever you need them — and me. You text me, it gets handled. No call centers, no tickets."

Costs you: ~$1/mo domain (amortized) + your landingsite.ai plan divided across all clients + minutes of your time. At 10 clients, that's ~$500/mo nearly pure margin. At 30, it's a salary floor. **The $800 build is the sale; the $50/mo is the business.**
