<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

---
title: "Market Scenario: The Ninety-Day Map"
date: 2026-04-08
slug: the-ninety-day-map
stream: market-scenario
tags: [thin-markets, market-design, ai, case-study, scenario, cosolvent, commoncontext, marketforge]
summary: A woman released from federal incarceration faces a dozen agencies, each with separate eligibility rules, clashing timelines, and no shared intake. A MarketForge-powered platform generates the one thing nobody gave her — a map.
estimated-read: 10 min read
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/the-ninety-day-map-hero.jpg" alt="A hand-drawn dependency chart on scattered government forms — the informal map of reintegration." loading="lazy">
  <figcaption>A checklist of benefit applications, shelter referrals, and parole reporting deadlines. The paperwork of reintegration.</figcaption>
</figure>

## Act A — The Map Nobody Makes

In Ontario, when someone is released from a federal penitentiary, Correctional Service Canada gives them a cheque for $166.

That's the discharge grant. It hasn't changed meaningfully since the 1980s. It is meant to cover the first days of reintegration — transit fare, a phone call, something to eat.

What it cannot cover, and what nobody provides at the gate, is a map.

The map would look something like this: to be eligible for transitional housing through the Elizabeth Fry Society, you need a confirmed parole address. To have a confirmed parole address, your parole officer needs to approve it. To get the parole officer to approve it, you need a letter from the housing organization confirming acceptance. To get that letter, you need to apply. To apply, you need a piece of government-issued ID. If your ID expired while you were inside, you need a birth certificate to renew it. If you were born in another province, that's a separate application, a separate fee, and a wait of three to six weeks.

Meanwhile the clock is running on your temporary absence conditions. Meanwhile ODSP eligibility, suspended at intake, cannot be reinstated until you have a mailing address. Meanwhile the employment readiness program at your community resource centre — the one with four funded seats specifically for people transitioning from federal custody — has an intake window of the 15th and the 30th of each month, and if you miss it by four days, you wait another two weeks.

None of these agencies coordinates with any of the others. Each operates a separate intake system, serves a separate mandate, and reports to a separate ministry or funder. The case manager you had inside — if you had one — has no formal relationship with the agencies outside. The agencies outside have no formal relationship with each other.

The person in the middle of this system is expected to coordinate it all. On day one. With $166, an expired ID, and a parole reporting appointment at 9am.

This is not a story about individual failure. It is a story about a market — a market that should exist, where agencies with funded capacity and people with genuine, urgent need should meet — that fails to function because the matching and sequencing infrastructure does not exist.

What follows is a fictional account of what it might look like if it did.

---

## Act B — The Story

### Leticia

Leticia Fontaine had been a medical billing specialist for eleven years before her conviction. She knew how to read eligibility matrices. She knew how to navigate claims systems built by people who had never tried to use them. She had spent a career decoding the bureaucratic language of healthcare institutions on behalf of patients who couldn't.

She told herself this would help.

On the morning of her release from Grand Valley Institution for Women in Kitchener — four years, a fraud conviction related to an employer billing scheme she'd been peripheral to, fully served — she walked out with a clear plastic bag containing her personal effects, her $166 cheque, and a two-page printed sheet titled *Community Resources — Waterloo Region and GTA*.

The list had twenty-three entries. Phone numbers. No web addresses. No hours. No eligibility notes.

Leticia knew what the list was. It was the map nobody made. A starting point so vague it was almost worse than nothing — it told her services existed without telling her which ones she could actually access, in what order, with what documentation, on what timeline, given her specific situation: federal release, no criminal record suspension yet, Waterloo-region parole jurisdiction, no confirmed home address, prior ODSP file that had been closed at intake four years ago.

She sat in the transit shelter across from the institution and called the first number on the list. Voicemail.

The second number rang through to a shelter intake line that told her the waitlist was currently eight to twelve weeks. She asked if there was something faster for women on federal release. The intake worker, not unkindly, said she'd need to call Elizabeth Fry directly.

She called Elizabeth Fry. It was 8:47am. They opened at 9.

She called her parole officer next, because reporting was mandatory and the appointment was at 9. The parole officer told her to have a confirmed address within five business days or a residential condition review would be initiated.

Five business days.

She was still in the transit shelter. The cheque in her hand was not cashable without ID. Her driver's licence had expired in 2023.

### The Intake That Wasn't

Leticia's situation was not unusual. It was, by the measures of anyone who worked in the reintegration sector, entirely typical.

What made it structurally impossible to resolve quickly was not any one missing resource — it was the sequencing. Housing required parole approval. Parole approval required housing. ODSP reinstatement required a mailing address. The employment readiness program required stable housing as a precondition. The criminal record suspension application — which would, eventually, allow her to work again in any role requiring a background check — had a processing timeline that could not begin until the remaining sentence conditions were met, and meeting them required a stable address, which required housing, which required—

A social worker at Elizabeth Fry named Amara Diallo had been working in reintegration services for nine years. She knew the loop by heart. She called it "the address trap." She had a whiteboard in her office where she had mapped, over time, the dependency graph of every intake requirement she regularly encountered: which applications had to come before which, which funding windows were time-gated and in which direction, which agencies would accept a conditional address and which required a confirmed one.

The whiteboard was impressive. It was also entirely in her head, assembled from nine years of navigating the same maze with different clients. When she went on leave, the whiteboard stayed behind. Her colleagues had their own versions — different, partially overlapping, each representing a different set of cases navigated over a different number of years.

There was no shared version. No platform that held it. No intake system that could read Leticia's situation and generate a sequence.

### The Platform

The Reintegration Pathways pilot — a joint initiative of the Ontario Ministry of Community Safety and Correctional Services, the Elizabeth Fry Society of Ontario, and a federal community reintegration grant administered through Public Safety Canada — had been running for eight months when Leticia was released.

It was not a case management system. The distinction had been fought over hard during the design process, and the Elizabeth Fry Society had held the line: a case management system monitors and tracks a person. This was a referral sequencing tool. It held no ongoing information about any individual beyond what they consented to share for the purposes of generating a plan. Once the plan was generated and accepted, the data was not retained by the platform.

Amara had learned about it three months before Leticia's release, at a sector briefing. She had been cautiously skeptical — reintegration workers had seen well-intentioned technology initiatives before, most of which had been built by people who had never sat in a transit shelter at 8:47am with an expired ID.

This one was different in one specific way: it started from the sequencing problem.

The platform's CommonContext layer — the curated domain knowledge base maintained by the platform's operator — held eligibility rules, intake windows, documentation requirements, and dependency logic for forty-seven relevant service categories across Ontario's twenty-three community service districts. Not a generalized database of social services. A specific, maintained, policy-versioned map of what required what, when, and in what order — built in partnership with the agencies themselves, validated against actual policy documents, and updated quarterly when rules changed.

Amara could access the platform's intake module through a secure browser. She could enter a client's situation — jurisdiction of release, sentence type, outstanding conditions, documentation status, benefit history, employment background, housing preference — without entering any identifying information at all. The system would return a sequenced service pathway: not a list of resources, but an ordered roadmap of which applications to file in which sequence, which intake windows to target, which dependencies to resolve first, and where conditional or simultaneous steps could be taken to compress the timeline.

She had used it four times. Each time, she had found at least one dependency or timing interaction she hadn't known about — not because she was uninformed, but because the rules genuinely changed between her cases, and no single person could hold all of it.

When Leticia called Elizabeth Fry at 9:02am, Amara answered.

### The Ninety-Day Map

The intake conversation took forty minutes. Amara entered Leticia's situation into the platform — not her name, not her date of birth, not her case number. Her release type (statutory release, federal, women's institution), her jurisdiction (Waterloo-region parole), her documentation status (expired Ontario driver's licence, no recent ODSP file, birth certificate on file from Québec), her employment background (medical billing, licensed healthcare administrator, registration currently suspended), her housing preference (Waterloo-region or GTA), and two specific constraints Leticia named herself: she couldn't be placed more than ninety minutes from her twelve-year-old daughter, who was living with her mother in Hamilton, and she would not accept placement in a shelter that required participation in religious programming.

The platform returned what it called a Sequenced Reintegration Plan. Amara printed it. It was four pages.

Page one was the first two weeks: the two things that had to happen before anything else could proceed. First, an emergency Ontario Photo Card application through ServiceOntario, which could be initiated with the institutional release documents and processed in five business days — Leticia hadn't known this option existed, and Amara hadn't known it had been extended to federal release documents seventeen months ago when the policy changed. Second, a conditional parole address using Elizabeth Fry Hamilton's transitional housing program, which had two beds available and accepted conditional parole submissions pending ID confirmation — which Amara also hadn't known until the platform surfaced it five minutes earlier.

The Hamilton placement solved the proximity constraint. The conditional submission broke the address trap.

Pages two through four laid out the following eleven weeks: ODSP reinstatement (day 8, once the photo ID was issued), employment readiness program intake at Hamilton-Wentworth John Howard Society (day 14 brought them inside the next intake window), healthcare administrator retraining referral through a workforce development program she was eligible for as a federal releasee (day 21), criminal record suspension pre-application counselling (day 45, the earliest it could productively begin), and a timeline for each subsequent step through to day 90, including the earliest plausible date for each and the dependencies that governed it.

The plan included things Amara would not have thought to include. A note that the Hamilton transitional housing was within the parole district, preserving Waterloo-region jurisdiction. A flag that Leticia's medical billing background made her eligible for a specific healthcare workforce re-entry track that most employment programs didn't know existed. A note that the criminal record suspension application interacted with the healthcare administrator registration process in a specific sequence — the suspension had to be submitted before the registration review, not after, or the review board would close the file and require a twelve-month wait.

That last note, alone, saved a year.

### The Generative Match Story

Alongside the sequenced plan, the platform generated what it called a Transition Narrative — a plain-language document addressed jointly to Leticia and to the Elizabeth Fry intake worker who would be supporting her. It described how Leticia's specific background interacted with her specific situation, across the specific services and timelines identified in the plan, and what the realistic twelve-month outcome looked like if the plan was followed.

The Transition Narrative was written from the perspective of neither party. It was not a case assessment of Leticia. It was not a service capacity report for Elizabeth Fry. It was a shared starting point: a description of how this specific combination of person, circumstances, services, and sequencing could, plausibly, lead to a particular outcome.

It noted that Leticia's medical billing background was a genuine asset — not in a generic motivational sense, but specifically: the Hamilton region had three medical clinics actively seeking certified billers, one of which had a program for hiring releasees from federal custody with healthcare backgrounds. The note identified the clinic by category (family health team, Hamilton Mountain area) and the relevant contact program (Ontario Works Enhanced Employment program, healthcare stream). It did not name the clinic. It provided the referral pathway.

Leticia read the Narrative carefully and said nothing for a moment.

Then she said: "Did you write this?"

Amara said no — most of it came from the platform.

Leticia said: "Somebody finally read the file."

Amara didn't correct her. In a sense, it was true. Forty minutes of structured intake, processed against a maintained knowledge base, had produced more contextual specificity than four years of institutional case notes.

### Day Ninety

Leticia started work as a billing specialist at the Hamilton family health team on day eighty-seven. The position was part-time initially, then converted to full-time at week sixteen. Her parole conditions were met, her ODSP was transitioning off by month four as her income stabilized, and her criminal record suspension application was in process.

None of this was guaranteed by the plan. The plan was a map, not a contract. Two things had gone sideways — the photo ID had taken nine business days, not five, because of a system issue at ServiceOntario, and the employment readiness program had moved its intake date by one week. Both required adjustments.

But Amara had the map. When something slipped, the map showed her where to re-sequence, what downstream effect the change had, and what contingent options existed.

That, more than any single referral, was what the platform had actually provided.

---

## Act C — The Structural Reading

This story is fictional. Leticia Fontaine and Amara Diallo do not exist. But the market failure they illustrate is real and is documented in reintegration research across Canada, Australia, and the United Kingdom.

The reintegration social services market exhibits every force of structural thinness — but its most important and least-discussed force is one that rarely appears in policy reports:

**Sequencing opacity.**

It is not that the services don't exist. It is not primarily that they are underfunded. It is that the dependency logic among them — which one must come before which, which intake window closes which door if missed, which applications interact in which order — is held nowhere systematically. It is distributed across thousands of individual workers' professional memories, rebuilt from scratch with each new client, and lost whenever a worker leaves.

This is exactly what the whitepaper on thin market theory calls **market memory fragility**: the accumulated knowledge of how a market works is held in human brokers rather than institutional infrastructure, and it evaporates with turnover. In a commercial market, broker turnover is costly. In a reintegration services market, it can cost a person a year of their life.

The other forces are also present:

**Regulatory fragmentation.** Reintegration touches at least four provincial and federal funding streams, each with separate eligibility rules, documentation formats, and intake timelines. No single agency has authority over all of them. The person at the centre of the system is expected to be the integrator.

**Cognitive overload, asymmetric.** The person navigating the system has the highest stake in getting it right and the least cognitive bandwidth to do so — not because they are incapable, but because they are doing it on day zero, in crisis, with no prior map. The agencies hold the information but not the overview. Nobody holds both.

**Trust deficit, dual-sided.** Agencies are cautious about sharing information across organizational boundaries — jurisdictional concerns, privacy regulations, liability. Individuals are cautious about sharing information with agencies because they have experienced the consequences of institutional disclosure. The trusted intermediary — the Elizabeth Fry worker, the parole officer — holds trust with both sides but cannot be everywhere simultaneously.

**Participant scarcity.** The pool of agencies with funded capacity specifically for federally-released individuals is genuinely small. The pool of individuals who meet the eligibility criteria for specific specialized programs — healthcare workforce re-entry, women's federal releasee transitional housing — is also small. The match between them is not impossible. It is just invisible.

The platform described in this story is a sequencing and referral tool, not a case management system. The distinction is not semantic. **A case management system monitors a person over time; a sequencing tool generates and hands off a plan.** The ethical architecture requires that distinction: this population's data cannot be held, aggregated, or retained without consent and without specific purpose. The thin market engineering intervention here is not surveillance — it is cartography. Making the map that nobody makes.

The CommonContext layer — the maintained, policy-versioned dependency graph of service eligibility and intake sequencing — is the core innovation. It is also the kind of knowledge curation that no individual agency can sustain alone but that a sponsored, sector-wide platform can maintain on their behalf. The natural sponsor is a consortium: provincial and federal justice ministries, the Elizabeth Fry and John Howard Societies, and university-based social innovation programs with the research capacity to maintain and validate the knowledge base.

Toronto Metropolitan University's Social Ventures Zone is exactly the kind of institutional environment where a venture like this could be incubated — where the proximity to both the justice system and the social services sector, and the university's research infrastructure, could sustain the knowledge curation work that makes the platform real.

The technology is not the hard part. The map is.

---

*The characters and organizations in this story are fictional. Grand Valley Institution for Women, the Elizabeth Fry Society, the John Howard Society, ODSP, Ontario Works, ServiceOntario, Correctional Service Canada, and Public Safety Canada are real institutions. Their programs, eligibility rules, and timelines are accurately characterized as of the date of publication.*

*DeeperPoint is developing the open-source tools that underpin platforms like the one described here. Learn more about the [thin market problem](../thin-markets.html), the [MarketForge platform](../marketforge.html), and [who these tools are designed to serve](../who-should-care.html).*
