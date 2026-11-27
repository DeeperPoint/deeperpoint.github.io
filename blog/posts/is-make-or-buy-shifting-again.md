---
title: "Engineer's Log: Is Make or Buy Shifting Again?"
date: 2026-11-27
slug: is-make-or-buy-shifting-again
stream: engineers-log
tags: [ai, explainer, scenario, canada, founders]
summary: "For software, the make-or-buy decision settled on buy a long time ago. AI coding tools may reopen it, not for the systems a business runs on, but for the discretionary work around them that was never worth a vendor search. A stamping plant's gas bill shows how."
estimated-read: 8 min read
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/is-make-or-buy-shifting-again-hero.jpg" alt="A plant engineer at a rolling bench with a laptop, looking across a factory floor at a compressor, a forklift and an open dock door" loading="lazy">
  <figcaption>AI-generated illustration</figcaption>
</figure>

**Author:** Mustafa Uzumeri

---

## A decision that went quiet

Make or buy used to have a seat in every discussion of manufacturing and operations. For parts and processes it still does. For software, the answer became close to automatic: buy. No equipment maker staffs up to write the code inside every subsystem, and nobody writes their own ERP. Tier one suppliers and enterprise software vendors do that work better, faster and cheaper.

Most of that still holds. Nobody is going to cancel an SAP licence because AI coding tools exist. My question is about everything else.

## Buying was never just the price

Buying software for a small job costs far more than the licence. There is the vendor search, the demos, procurement, the security review, the contract, and then a project to connect the new tool to what is already there. For a large system that overhead is worth paying. For a small job it is often bigger than the job, so the job is never done.

One or two people working with AI tools can now build a small, specific piece of software in days. When the build costs less than the paperwork of buying, the decision reopens. It reopens at the edge of the business, not at the core.

## Mission-critical and discretionary

The line I would draw is between mission-critical systems and discretionary ones. The test is simple: if this stopped working tomorrow, would the operation still run?

For mission-critical systems the risk and the reward do not favour making, and I expect that to change slowly, if at all. Discretionary does not mean low value, though. It means the business can try something, be wrong, and switch it off without missing a shipment.

Software is now inside a huge number of physical products, and that is where the discretionary opportunity looks largest to me. A story shows it better than an argument.

## The January gas bill

*This story is invented. The plant, the people and the numbers are fictional. The equipment, the vendor portals and their limits are ordinary.*

Kestrel Metalform is a 140-person stamping plant in Cambridge, Ontario. One morning in February the controller put the January gas bill on Marta Kowalczyk's desk. It was 30 percent higher than the January before, and the winter had not been colder; Marta, the plant engineer, checked. The heating contractor inspected the rooftop units that warm the incoming air and found nothing wrong.

Marta had a guess: the shipping doors. A guess was not enough to change how the dock worked, and the evidence was in four places that had never met.

- The dock doors had sensors, and the door company's portal showed when each door was open.
- The forklifts were leased, and the dealer's portal showed where each truck was and whether it was moving.
- The rooftop units reported to the controls contractor's portal, which showed how long each burner ran.
- The shipping appointments were in the ERP.

Each system answered questions about itself. None could say why door 4 was open.

She asked the vendors. The door company offered a custom report, in six weeks, for a fee, covering doors only. Nobody sold the thing she wanted, and nobody ever would: it was a question about one dock at one plant.

So she made it. Marta is not a programmer. Over a week of afternoons, working with an AI coding assistant, she built a small program that ran each night. It collected the day's door history, forklift log, burner hours and shipping appointments and put them on one clock. She worked only from the files the portals let her download, and never connected anything to the plant's own network. Before she trusted it, she stood on the dock for a shift with a clipboard and checked the program's version of that day against her own.

The answer was there within a week. Door 4 was open a little over three hours a day, and a trailer was backed up to it for less than one. The second shift opened the door at the appointment time, as the procedure said. One carrier usually arrived an hour late. The forklifts waited nearby, and the burner above the dock ran flat out until the trailer sealed the opening. Nobody was doing anything wrong.

The fix was not software. The gatehouse now radios shipping when the truck is at the gate, and the door opens then. Door 4's open time fell to about an hour and a quarter a day. Marta puts the saving at roughly $2,300 a month through the winter.

Three things happened next, and they matter as much as the saving.

The shift supervisor asked whether the program could simply close the door when no truck was there. Marta said no. A program that reads a door's history can be wrong without hurting anyone. A program that moves a dock door is a safety system, and it belongs to the people who build those.

The controls contractor's portal turned out to have no bulk download. Burner hours came out one unit and one month at a time, by hand. The contractor quoted a price for a proper data feed. That boundary had nothing to do with technology.

And the plant manager asked who would look after the program when Marta was on holiday, or gone. So far the answer is a two-page note and one colleague who has run it once. That is a start and not yet an answer.

By spring, other departments had brought her eleven more questions.

## What the story is for

Every piece of that story is small. The saving would not have justified a software purchase, a consultant or an integration project, which is why it had gone unmade for years. It became worth doing only when the cost of making fell to one capable person and a week.

It also only read data the equipment was already producing. The stamping presses, the ERP and the doors themselves were untouched. That is what I mean by discretionary.

## Where I would be careful

Marta ran into three of the objections herself. A fourth is older than she is.

- **We have been here before.** Spreadsheets, departmental databases and low-code tools each produced a wave of in-house building, and each left behind tools nobody owned once their author moved on. Writing software was never the expensive part. Owning it for ten years was. AI makes it cheaper to read and repair someone else's code, but it does not decide who is responsible for it.
- **Discretionary tools do not stay discretionary.** A useful one gets depended on. The moment an in-house tool sends instructions back to equipment, it is part of operations and should be treated that way.
- **The data is not always yours to read.** Much of it sits in the equipment maker's cloud. Vendors control the access, the limits and the terms. Some boundaries are there on purpose.
- **Reading is not always free of risk.** Marta stayed off the plant network. A tool that asks equipment for data directly has to be built with care, and the people who run that network will rightly want a say.

## One data point

I can offer one piece of real evidence, and I want to be exact about what it shows. The DeeperPoint tools (a marketplace engine, the knowledge wikis behind it, two working demonstration markets and the analysis tools around them) are about eighteen months of work by one person using AI tools, with a little back-end help. Ten years ago I would have guessed a team and a budget.

That shows how much one person can now produce. It does not show how such software holds up under years of maintenance or at enterprise scale. I do not know that yet, and neither does anyone else.

## The question

So is in-house development about to have a renaissance? At the core of the business, I doubt it. Around the edge, in the discretionary work that connects systems and uses data nobody had time to use, I think it may already have started.

Two questions follow, and I will take them up in later posts. If companies make more, who sells less? And if suppliers lose work to in-house building, does the hiring on the buyers' side make up for it?

For the work this log usually covers, see [MarketForge](../marketforge.html).

<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->
