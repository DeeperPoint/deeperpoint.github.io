---
title: "Engineer's Log: The Black Widow Effect: When Big Customers Love their Suppliers"
date: 2026-03-16
stream: engineers-log
tags: [supply-chain, market-design, strategy, thin-markets]
summary: Why big companies' long payment terms can lethally damage their most valued small suppliers.
estimated-read: 7 min read
slug: the-black-widow-effect
---

This is a very long post. Longer than I normally write. But I believe it explains a concept that is critically important to purchasing and supply chain system design. Many big companies seem to understand this. Some do not. Quite a few smaller suppliers need to know it.

If you work for a big company that offers a mature invoice financing system that it is open to every supplier, regardless of size or financial stability, you may already understand this. If you aren’t quite sure why your company needs that program, this will help to explain it.

If your company doesn’t offer an invoice financing system, or if it limits the service to “approved” suppliers, **you owe it to yourself to read this**. Your actions, and the actions of your company, may be inflicting unnecessary and possibly lethal damage on suppliers you value highly.

If you work for a small supplier, chasing that big, long term contract, **you absolutely must understand the concept in this post**. Your survival may depend on it.

## Scenario

Imagine that you work for BIGCO and you want to buy a product or service. It’s not a commodity and you have to search a bit. Finally, you find a SMALLCO that does exactly what you want. You start with some small contracts. They exceed your expectations. You’re thrilled. 

You give them more work. Then still more work. You recommend them to other colleagues in BIGCO. Every delivery is outstanding. SMALLCO also seems to be charging healthy prices, so it looks like everyone is a winner. Orders continue to increase.

***Then SMALLCO goes bankrupt\!***

It’s tempting to think it was bad luck. Maybe SMALLCO was badly managed. Maybe they messed up on another contract. Maybe a calamity hit them. 

But it may not have been an accident and SMALLCO didn’t (willingly) commit suicide. **You and BIGCO may have killed it**. And the more business you sent, the faster you drove it out of business 

… *IF BIGCO is imposing longer payment terms on its vendors.*  

## Context

Anyone who has worked on either side of the B2B buyer/seller relationship knows that large companies are increasing their payment terms. This isn't just anecdotal; recent data paints a stark picture of a global shift toward longer payment periods as big companies prioritize preserving their own cash:

* **Global Working Capital at Crisis Levels:** According to a 2024 report by Allianz Trade, the average global payment term reached 62 days, pushing the global working capital requirement to 78 days—its highest level since the 2008 financial crisis.
* **The "Pay Later" Default:** In Europe alone, companies collectively extended an additional €11 billion in credit to their business partners between late 2024 and early 2025 simply through longer payment terms.
* **Shifting Standards:** In the United States, while "Net 30" remains a common standard, there is a noticeable shift toward "Net 60", particularly among established retailers. Larger firms are increasingly taking 60 to 90 days to pay. Meanwhile, in the Asia-Pacific region, "ultra-long payment delays" (over 180 days) are anticipated to increasingly become the norm.
* **Informal Lenders:** Experts predict this trend will only worsen into 2026. This practice essentially turns small companies into informal lenders to their massive corporate customers, drastically raising the risk of supplier defaults and bankruptcies.

While many big companies are lengthening their supplier payment terms, the smarter ones have set up vendor invoice financing systems to help limit the damage to their suppliers.  In these systems, the buyer (or third party) typically advances payment of buyer-approved invoices (minus interest and fees) to suppliers who want faster cash. Factoring companies have been doing this forever.

*FWIW, my personal favorite approach is the type of solution that is offered by [Orbion](https://www.orbian.com/). Orbion directly hooks its computer to various BIGCO computers and sells BIGCO’s approved invoice payment (i.e. BIGCO’s payment promise) to the London financial markets as “commercial paper”. It gives (most) of the cash immediately to the supplier. It is cheaper and faster than traditional invoice factoring arrangements and most supplier advance payment terms.* 

## What Happens to Cash in A Sales Relationship?

When a BIGCO establishes purchasing expectations and payment terms to (especially small) vendors, it effectively controls the structure of the SMALLCO cash flow. I can demonstrate this with a simple model of supplier cash flow. You can download [the spreadsheet to experiment for yourself](http://deeperpoint.com/wp-content/uploads/2014/12/BlackWidowPaymentCalcs.xlsx). 

<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-1.png" alt="Chart 1" loading="lazy">
</figure>

The spreadsheet has 3 variables: 

* Percent price markup  
* How quickly sales are expected to grow (year over year) to that supplier  
* Effective Payment Lag (in months) from customer to supplier

There are only 2 rows of active values … revenue and expense. Everything else is just addition. Yet, the model shows that long payment terms, combined with rapid sales growth can create a dangerous combination. The three key variables are as follows:

### Effective Payment Lag

The vendor’s cash commitment to honor each order typically follows a consistent pattern. When SMALLCO receives the order it starts spending cash to produce the item or service. When SMALLCO has completed and delivered the order, it invoices BIGCO and waits for payment. 

<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-2.png" alt="Chart 2" loading="lazy">
</figure>

The payment lag can be estimated several ways:

* **It can begin at order**. That is appropriate if you believe that, by taking the order, the vendor is **committed** to set aside enough cash to fund the transaction.  
* **It can begin at delivery**. That is the view conventionally taken by large buyers. It ignores the tied-up cash that precedes that date.  
* **It can begin somewhere between order and delivery**. This would split the difference and might reflect that the vendor doesn’t have to actually spend all of the cash immediately. In theory, it can finesse the timing of its cash flow a little bit if it has several orders that overlap.

Rather than try to justify one of these assumptions, I adopted the single variable “effective payment lag”. It captures the sum of the vendor and payment term lag. Make whatever assumptions you feel are appropriate and plug the total time into the spreadsheet. If you feel that the vendor is on the hook for the cash at order and it takes 2 months to complete the work and the buyer payment terms are 2 months, the effective payment lag will be 4 months. If you felt that the vendor was only committed halfway through the production cycle, then the effective lag would be 3 months. Make your own assumptions and plug your own number into the yellow cell.

Note: To simplify calculation, the spreadsheet only accepts integer months up to 11 for the payment lag. 

### Sales Growth

If you (as BIGCO) really, really love SMALLCO, you will probably order more from them after a year’s time. How much more? 1.5 times? 2 times? 3 times? Plug that number into the spreadsheet in the green cell. The monthly compounding growth rate appears in the pink cell below it.

### Vendor Markup (aka Price)

The vendor markup is the percentage added to the vendor’s cost of goods sold (COGS) to arrive at the price. If the vendor’s direct materials and labor costs are x and the markup is 60%, the selling price will be 1.6x. Plug the percentage markup in the blue cell.

## So what can happen?

The spreadsheet reflects these three assumptions to generate a graph of SMALLCO’s cumulative cash flow on a continuing stream of orders that it accepts from BIGCO. The fun is to play with the numbers and see what happens. The following table gives some interesting combinations, with possible assumptions and comments on the outcome.

| Assumptions | Cumulative Cash Flow | Comments |
| ----- | ----- | ----- |
| **<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-3.png" alt="Chart 3" loading="lazy">
</figure>** | <figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-4.png" alt="Chart 4" loading="lazy">
</figure> | BIGCO buys a steady amount and pays promptly SMALLCO has minimal investment and steady cash growth |
| **<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-5.png" alt="Chart 5" loading="lazy">
</figure>** | <figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-6.png" alt="Chart 6" loading="lazy">
</figure> | BIGCO buys more, but pays promptly SMALLCO still has minimal investment, but its cash reserves grow very quickly |
| **<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-7.png" alt="Chart 7" loading="lazy">
</figure>** | <figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-8.png" alt="Chart 8" loading="lazy">
</figure> | BIGCO extends payment terms one month SMALLCO suddenly needs 7 months to recover its initial cash investment |
| **<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-9.png" alt="Chart 9" loading="lazy">
</figure>** | <figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-10.png" alt="Chart 10" loading="lazy">
</figure> | BIGCO extends payment terms another month.  It now takes 13 months for SMALLCO to regain cash neutrality |
| **<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-11.png" alt="Chart 11" loading="lazy">
</figure>** | <figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-12.png" alt="Chart 12" loading="lazy">
</figure> | BIGCO extends payment terms for another month. **SMALLCO faces a deep initial cash drain and it may take years to catch up** |
| **<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-13.png" alt="Chart 13" loading="lazy">
</figure>** | **Black Widow Effect** <figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-14.png" alt="Chart 14" loading="lazy">
</figure> | BIGCO accelerates purchases and keeps its extended payment terms. **SMALLCO faces a permanently deteriorating cash position** |

From my trials, there were a couple of key observations:

* Nothing too serious ever happens if the payment lag is small.  
* Vendor cash position **can react in a non-linear fashion** to changes in growth or payment lag. This is a biggie. Non-linear relationships usually create surprises, often nasty ones.  
* Increasing the markup (i.e., price) does not help nearly as much as one might expect.

## What is really happening? 

The spreadsheet assumptions and outcomes fall into four major categories and I have tried to diagram the ones that are less intuitive.

### Traditional and Conventional

Move along, nothing to see here. 

BIGCO buys at a reasonably steady rate, pays reasonably promptly (30 days or so), and/or allows for progress payments or other cash supply mechanisms. SMALLCO may have to invest a bit of cash to get the contract, but it gets it back pretty quickly and builds a steady cash surplus around BIGCO’s business.

### Vendor as Bank

If BIGCO starts to extend its payment terms and increases its purchases, it can quickly create a situation where the vendor is “financing” part of the transaction, possibly for a long time and possibly for growing amounts.

In this scenario, the long term prospects for SMALLCO are good, but it must find a chunk of cash to get through a startup phase that can be surprisingly long. Under fairly plausible assumptions, SMALLCO may have its cash tied up for a year or more. That can hurt SMALLCO’s ability to grow as a company (something BIGCO would probably like to encourage if SMALLCO is really that good). 

<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-15.png" alt="Chart 15" loading="lazy">
</figure>

This diagram illustrates why there are also some weird aspects to the arrangement. The transaction assumes that BIGCO is placing regular orders that are growing in total volume over time. With the payment lag (L), SMALLCO has to put in up front cash (pink). It will start to generate free cash only after lagged payments begin (blue). For as long as the relationship exists, SMALLCO will be owed more and more cash by BIGCO … cash it cannot enjoy because it is constantly having to spend cash ahead of the growing BIGCO payments. There are two weird parts of this arrangement. 

* SMALLCO is financing a growing cash “loan” to BIGCO. In most cases, BIGCO would have a much lower cost of capital than SMALLCO. This system embeds the principle that the funds are being invested or borrrowed **at the highest cost of capital**. That doesn’t seem very sensible.  
* The only one way that SMALLCO can collect all of the cash that is owed to it is **if it stops selling to BIGCO\!** That also doesn’t seem like a suitable incentive for a beloved supplier.

The spreadsheet shows that it is surprisingly easy for a sales relationship to wander into this territory. 

### The Critical Position

If we keep moving the assumptions in the wrong direction, we can get to a point where the growth rate and payment lag effect exactly offsets SMALLCO’s profit margin. 

At this point, SMALLCO will be constantly committing more cash that it will **never** get back **unless it stops working for BIGCO**. 

<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-16.png" alt="Chart 16" loading="lazy">
</figure>

The condition where this occurs is simple to estimate. It is the point where the m=Lr equation is true. At this point, SMALLCO has to spend continually increasing amounts of money to service the contract, but the lagging monthly payments just matches these rising costs. Theoretically SMALLCO could be stuck at cash break-even forever … or at least until it terminates the contract and waits for its well-earned excess cash to finally roll in. 

It makes me want to paraphrase the signature line from the movie War Games: **The only way to win the game is to stop playing\!**

### The Black Widow

If BIGCO pushes SMALLCO past the Critical Position, SMALLCO is on a fast track out of business. The only way it can accept more orders is to go to the bank and borrow more money (at its higher cost of capital) to front the ever-increasing production expenses.

<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-17.png" alt="Chart 17" loading="lazy">
</figure>

No banker I can imagine is going to front working capital to a sales transaction that can only pay off if SMALLCO stops selling to BIGCO. If the banker does put up with it for a while, the cost of capital will surely be rising for every new borrow.

**This, quite clearly, is nuts.  No one wins.  Except maybe a bank … for a little while.**

Yet, it is not hard to imagine plausible scenarios where this can happen, especially if the BIGCOs of the world increase their payment terms without offering vendor financing relief. 

I plan to write a few follow-on posts to explore practical factors that might pull a sales relationship close to or past the critical position. But for now, this post is long enough. I look forward to thoughts and comments. If you can find a hole in my argument, that would be best of all. Then I wouldn’t have to worry about the SMALLCOs of the world.

<figure class="blog-figure">
  <img class="blog-figure__img" src="../images/blog/the-black-widow-effect-18.png" alt="Chart 18" loading="lazy">
</figure>
