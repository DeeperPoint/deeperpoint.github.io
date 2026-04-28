# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.
# Generates history.html with expandable timeline cards (Option B)

import json, os

ENTRIES = [
    # Origins
    {"year":"1974","era":"origins","title":"Modeling Travel Demand for Toronto",
     "img":"ttc-map-toronto.jpg",
     "text":"I converted manual travel demand analysis into Fortran computation for one of Canada's first holistic metropolitan transportation studies."},
    {"year":"1976","era":"origins","title":"Light Rail Operating Strategies",
     "img":"ea15-20140819-Streetcar-UTDC.png",
     "text":"Ontario set up a company to build a Canadian light rail vehicle. I worked on the operating strategy for LRT lines. The company eventually moved to Kingston and was later bought by Bombardier as the basis for its light rail ventures over following decades."},
    {"year":"1977","era":"origins","title":"Subway Bid for Caracas",
     "img":"caracas.jpg",
     "text":"I worked for a year on the team that assembled a Canadian consortium bid to build the Caracas Metro. We lost the bid, but I did learn a lot of Spanish and traveled to Bogota and Caracas a number of times."},
    {"year":"1981","era":"origins","title":"Railroad Capital Investment",
     "img":"CPBridge.jpg",
     "text":"I got a job in the Research Group at Canadian Pacific Railways (CP) in Montreal. It was a type of internal consulting group and we tackled whatever weird issue arose. My biggest task was to rewrite the manual for cost-justifying capital projects at CP. In the process, I was schooled by the old-bull line managers that my MBA knowledge didn\u2019t quite cut it for investments that were expected to stand for 100 years or more."},
    {"year":"1983","era":"origins","title":"Selling Wind Tunnels",
     "img":"volvowindtunnel.jpg",
     "text":"I worked in business development at one of the 3 companies in the world that you would call if you wanted a wind tunnel. I worked on contracts and project scheduling and writing proposals \u2026 lots of proposals. Some were even accepted."},
    {"year":"1985","era":"origins","title":"Automating Wind Tunnels",
     "img":"scan-scaled-e1582756864287.jpg",
     "text":"I was the liaison (i.e. shock absorber) between the management of an old-school engineering company and a group of crazy, but brilliant systems engineers. The geeks invented a system, \u201cTalent\u201d that was probably 5 to 10 years ahead of its time. It ran as a network of distributed physical and virtual machines \u2026 with real time performance that was absolutely insane. I did the business development (i.e., made sales calls and wrote the sales proposals) for the systems and the technology. They later formed a company (ReAct Technologies) that absorbed the founding firm \u2026 and is still the global go-to company for ultra-sophisticated research test automation systems."},
    {"year":"1987","era":"origins","title":"One of the Last Tours of the Internet",
     "img":"hosts-file-windows-10-551x480-1.jpg",
     "text":"When I started my PhD in 1987, the Internet was still Arpanet. Every destination in the world was listed in a single text hosts file. I spent (wasted?) a couple of months hunting through every anonymous ftp site in that hosts file."},

    # Academic
    {"year":"1990","era":"academic","title":"Manufacturing Variety vs. Change (PhD)",
     "img":"SonyWalkman.bmp",
     "text":"This was my PhD dissertation. I examined how product families differed on the characteristic of product variety and serial design change. I found a pattern that was stable and logical that applied across essentially all of the discrete products industries \u2026 at least at that time."},
    {"year":"1992","era":"academic","title":"Analyzing Structure of Product Families",
     "img":"BookCovers.png",
     "text":"Susan Sanderson and I published a textbook (and a companion trade press clone). The textbook was adopted at University of Hong Kong, University of Singapore and MIT. I think we wrote it slightly above the mass market."},
    {"year":"1994","era":"academic","title":"Management Control Systems",
     "img":"NewmanControlDiagram.png",
     "text":"I began my fascination with the concept of management control and it has continued ever since. Academics don\u2019t like to talk about \u201ccontrol\u201d, but it is central to the management process and we need to understand it in all its forms."},
    {"year":"1994","era":"academic","title":"Population of Learners",
     "img":"3DMapOfLearners-scaled.png",
     "text":"I was given access to corporate training data for an apparel manufacturer. There were records of thousands of employees who were learning how to sew t-shirts and similar garments. David Nemhard and I developed a model of learning that modelled individual behavior as a stepping stone to modelling group behavior."},
    {"year":"1996","era":"academic","title":"Early Viral Internet Scandal (Intel Pentium)",
     "img":"scan0003cropped.png",
     "text":"Intel made a mistake with its Pentium chip and a university researcher caught them out. The resulting furor ultimately forced Intel to recall existing chips at a cost of at least $250 million. I used usenet and Internet chat records to document the process. It was probably the first scholarly analysis of what is now called a \u201cviral\u201d Internet scandal."},
    {"year":"1996","era":"academic","title":"Chrysler IDS Video Training System",
     "img":"IDSCropped-scaled-e1582810328410.jpg",
     "text":"Chrysler\u2019s Huntsville AL electronics plant spent nearly 2 years investigating and evaluating how to apply cutting edge video editing tools to the production of plant floor training materials. The original technology came from Quantel \u2026 a global broadcast video vendor. Although Chrysler ultimately declined to move forward, this project set me off on a 25 year quest to understand how video can be used in day-to-day business operations."},
    {"year":"1999","era":"academic","title":"Studying Learning AND Forgetting",
     "img":"Screen-Shot-02-27-20-at-09.49-AM.png",
     "text":"I collected large volumes of operator learning data at Chrysler. Two colleagues and I used that to build a model that accounted for patterns of learning, but also captured how performance was lost when a worker was moved away from the task."},
    {"year":"2002","era":"academic","title":"ISO 9001 Standardization",
     "img":"ISO_9001-2015_w.jpg",
     "text":"In the late 80\u2019s manufacturing companies around the world faced demands to adopt a manufacturing quality standard: ISO-9001 \u2026 then endure audits to certify they conformed. I was fascinated because academic theory said that management practice cannot be standardized. Yet thousands and eventually millions of companies complied. Either management theorists were wrong or the standards writers were using smoke and mirrors. I spent 7 or 8 years digging into the phenomenon to try to resolve the contradiction. I think I succeeded because I wrote 4 or 5 journal articles that were accepted at good publications."},
    {"year":"2006","era":"academic","title":"Space-Time Diagrams for Operations",
     "img":"Screen-Shot-02-26-20-at-09.58-AM.png",
     "text":"I had several German students visit Auburn to study with me. Alex, Steffi and Fabian. Not sure why I was chosen, but they were great kids and all went on to good things. Fabian took an interest of mine and developed it into a Master\u2019s thesis that was very thorough and coherent. It sliced and diced the concept of space-time diagrams as they applied to production and similar operations."},
    {"year":"2007","era":"academic","title":"Explaining AC Motors for Siemens",
     "img":"MovingStatorField2011.png",
     "text":"AC Motors are incredibly common and important. They are also amazingly simple and elegant, thanks to Nicola Tesla. However, it is no easy chore to explain them to non-engineers. I tried this for Siemens and I think I came pretty close to nailing it. This was the first project where I tried to use simplified visual models to explain a mysterious and obscure system."},
    {"year":"2009","era":"academic","title":"Black Widow Supply Chain Financing",
     "img":"BlackWidowDiagram-1.png",
     "text":"Since iPOV was always eagerly waiting for payments from big customers, I became interested in the implications of steadily lengthening payment terms. I ended up with a surprisingly simple model that largely upended all of the stuff we were teaching MBA students."},
    {"year":"2010","era":"academic","title":"Dimensions of Perception with Video",
     "img":"TaskDimensionsSpeed.png",
     "text":"I worked for a while with an industrial engineering PhD student and, from that interaction and with iPOV on the side, I commissioned a series of graphics that summarized what humans can see versus what a video camera can see."},
    {"year":"2012","era":"academic","title":"Teaching Outside to Inside",
     "img":"remoteInterview.jpg",
     "text":"Even before we moved to Atlanta, I was fascinated with the idea of using mobile networks to teach. Universities had been teaching remotely for years and I taught for 6 years in Auburn\u2019s Executive MBA. But on-campus students desperately need to see the reality of the outside world \u2026 and it is very hard to bring that back to campus. The occasional guest speaker doesn\u2019t really cut it. By 2012, the technology pieces fell into the puzzle. I hopped around Atlanta with a laptop, a webcam and Verizon 4G. I delivered live lectures from the floor of a shipping dock, from a trade show floor, from the offices of Home Depot and Chick-fil-A logistics executives. Reality baby!"},
    {"year":"2015","era":"academic","title":"Rethinking Higher Education",
     "img":"MBRIPuzzle.png",
     "text":"I was briefly drawn into the efforts of Morris Brown College to resurrect itself from oblivion. Their situation was dire, so I tried to think outside the box and find a teaching model that could work at much lower cost. Nothing came of it, but the exercise gave me some insights and ideas. My idea is to restructure Higher Ed so it stays true to its heritage, but uses new business tools to \u201cmanage\u201d how they teach the traditional subjects."},

    # iPOV
    {"year":"1997","era":"ipov","title":"Building eLearning Tech",
     "img":"sales-force.png",
     "text":"Over a 10 year period, iPOV developed a collection of cool web software tools for eLearning. Technologies included Flash ActionScript, XML, and video. Some of our best stuff used Flash to put dynamic, interactive layers over standard video. That wasn\u2019t really replicated in web video for at least a decade."},
    {"year":"1998","era":"ipov","title":"Employment \u201cFarm Team\u201d",
     "img":"Jobs.jpg",
     "text":"For a decade iPOV relied on work by part-time Auburn students. They so consistently exceeded expectations that most ended up in great jobs after graduation. Many of them credited the opportunities and mentoring they received at iPOV. From this experience, I evangelized for the concept that universities could support an ecosystem of \u201cfarm team\u201d companies for large employers. No one seemed interested, but I am still convinced it is an excellent and practical idea."},
    {"year":"1999","era":"ipov","title":"iPOV Processing Workflow",
     "img":"Slide1.png",
     "text":"iPOV developed a workflow for eLearning production that cut conventional development time and cost by at least 75%. It remained iPOV\u2019s hallmark for nearly 20 years. I still use it today for my personal work."},
    {"year":"2002","era":"ipov","title":"eLearning Design Patterns",
     "img":"Screen-Shot-02-27-20-at-12.21-PM.png",
     "text":"One of iPOV\u2019s secret weapons was a system of simple design patterns for eLearning. They were not so much designed to look good \u2026 although they could. They were designed to make it easy and foolproof to build material that was clear and accurate. We never really got our clients to grasp that point, which is too bad, but it really helped us cut costs."},
    {"year":"2004","era":"ipov","title":"Framework of Technical Explanation",
     "img":"ThreeTypesOfExplanations.png",
     "text":"iPOV made so many technical manuals (about 500 projects all told) that we became very methodical about their structure. I crafted a 2 page model that guided the structure of almost all of our materials. It was very versatile and seldom let us down."},
    {"year":"2004","era":"ipov","title":"Embedding Video in PDFs",
     "img":"Screen-Shot-02-27-20-at-12.31-PM.png",
     "text":"iPOV didn\u2019t invent this \u2026 Adobe did. However, iPOV pushed the idea hard and developed some software tools to make it faster and easier to author PDFs that contained embedded video. Originally, we used Flash video. Later, we did the same thing with mp4."},
    {"year":"2006","era":"ipov","title":"CoSolvent Video Gallery",
     "img":"Collage.png",
     "text":"iPOV developed a \u201cyoutube clone\u201d based on open source software. It was designed to make searching video much easier and faster \u2026 easier even than Youtube. It worked, and we used it extensively in our projects, but the death of Flash killed it too \u2026 even though we had switched everything to mp4, it was too late."},
    {"year":"2007","era":"ipov","title":"Video Speaks Every Language (Michelin)",
     "img":"MRT_retread.jpg",
     "text":"A Michelin subsidiary hired iPOV to build video courses on their operations. iPOV\u2019s methodical process made it easy to construct the courses \u2026 then translate them into other languages. We produced companion versions in French (for Quebec) and Spanish."},
    {"year":"2008","era":"ipov","title":"iPOV Flash Video Player",
     "img":"playlist.png",
     "text":"iPOV took Flash to its logical conclusion by creating a web video player that could be actively reprogrammed on the fly. We used it a lot ourselves, but we never really got traction trying to offer it to others. Poor marketing was a big part of that, but the growing resistance to Flash played a part. Eventually, we gave it away as open source."},
    {"year":"2008","era":"ipov","title":"The Day the Orchestra Went Home",
     "img":"financialcrash.jpg",
     "text":"The financial crash hit our big corporate customers hard \u2026 and iPOV was all but wiped out. We survived for a while, but debts crippled us until my wife and I paid them off a decade later."},
    {"year":"2009","era":"ipov","title":"Amgen Interactive Video System",
     "img":"REMSSystemOverview.png",
     "text":"iPOV\u2019s love affair with Flash hit a peak when we were asked to propose a system to Amgen. They didn\u2019t buy it, but the design was awesome \u2026 and we had all the pieces already working. The system would have interactively edited video snippets into polished sequences, depending on the preferences indicated by the viewer. Instead of watching a long training video with a lot irrelevant parts, you would see just exactly what you needed to see."},

    {"year":"2010","era":"ipov","title":"Explaining Material Master",
     "img":"Self-NavigatingMaterials.png",
     "text":"The idea of a \u201cmaterial master\u201d is central to the design of every major class of transaction management software: CRM, ERP, WMS, Payables, etc. Like AC motors, however, it is usually perceived as a mystery that most employees don\u2019t want to try to understand. iPOV came up with a pretty elegant, animated explanation."},

    # Recent
    {"year":"2011","era":"recent","title":"Surveillance of Operations (Dartfish)",
     "img":"Surveillance-1.png",
     "text":"I worked with a sports video software company \u2026 Dartfish.com \u2026 to use video to observe and record business and factory operations."},
    {"year":"2013","era":"recent","title":"New eLearning Production Workflow",
     "img":"Screen-Shot-10-11-17-at-11.11-AM.png",
     "text":"When I shut down the Auburn iPOV operation, I had to invent a new eLearning production process that would work with remote freelancers. To make the system more appealing to corporate clients, I set it up to use Adobe Creative Suite and Microsoft SharePoint. With the advances that have occurred in both sets of tools, it actually works pretty well."},
    {"year":"2013","era":"recent","title":"Fluid Projects (Global Freelancers)",
     "img":"OutsourcingModel.png",
     "text":"After iPOV closed up shop in Auburn, I engaged in a number of projects out of Atlanta. My new business model was to use teams of freelancers from all over the globe. If it sounds risky \u2026 it isn\u2019t."},
    {"year":"2013","era":"recent","title":"Video for Operations Analysis",
     "img":"StoreSurveillanceSnippets.png",
     "text":"I worked with an industrial bakery, Dartfish and Michael Darden to explore a variety of ways to use video to capture raw data for operations analysis. This didn\u2019t really lead to any dramatic opportunities, but it offered tremendous promise and was very interesting."},
    {"year":"2014","era":"recent","title":"Software Sales Training (Siemens PLM)",
     "img":"Whats-the-Role-of-Teamcenter-in-the-PLM-Drive.jpg",
     "text":"I constructed seven detailed courses to train Siemens PLM sales personnel around the world. The courses covered sales techniques, product knowledge and corporate sales management. I also arranged to have them translated into 4 other languages."},
    {"year":"2015","era":"recent","title":"Using Video to Teach Soft Skills",
     "img":"bigstock-Handshake-Hand-holding-on-bl-43772743.jpg",
     "text":"I developed sales training courses for a global multinational tech company. There were a lot of courses, so they must have been happy. The key to my design was to use video to explain complex situations that text and graphics could not capture."},
    {"year":"2016","era":"recent","title":"Event Mapping Utility",
     "img":"gallery.png",
     "text":"For about a year, I wrangled the team of developers (in Algeria and Mexico) to create a flexible event mapping utility. It was totally responsive so it ran on desktops and mobile. It also fed anonymous data back to a database where we could build maps of visitor behavior."},
    {"year":"2017","era":"recent","title":"Factory Surveillance System",
     "img":"frontimage.png",
     "text":"A friend owns an industrial bakery. I talked him into installing some surveillance cameras and a decently capable video management system to observe operations \u2026 particularly in his production machinery. A lot of weird things can happen with waffle and pretzel dough and there isn\u2019t always a person nearby to see it."},
    {"year":"2018","era":"recent","title":"IoT and Factory Video",
     "img":"DistributionOfGaps.png",
     "text":"I worked with a local industrial bakery to integrate IoT sensors into their suite of surveillance video. The idea was to recognize machine events from the factory floor and use that data to make it easier to find relevant video on the surveillance system. The project petered out for reasons unrelated to the technology \u2026 but I was able to assemble an effective proof of concept before things wound down."},
    {"year":"2019","era":"recent","title":"Stacks HOA",
     "img":"StacksHOA.png",
     "text":"I served as president of the Stacks Home Owner\u2019s Association. I lasted 13 months \u2026 one month longer than the previous record-holder."},
    {"year":"2020","era":"recent","title":"Phantom Data in Trucking",
     "img":"phantom-data-2x.png",
     "text":"I resumed work with Michael Darden and DFM Data Corp in a supportive role. DFMDC is tackling a hugely important problem that is beginning to surface in the US trucking spot market. The spot market arranges 500,000 to 1.5 million truck loads per day. My investigation resulted in two findings: a) the problem is real and big, and b) the way the DFM industry works, it is really hard to fix unless we can institute a reliable ID on planned truckloads before they enter the negotiation and bidding system."},
    {"year":"2021","era":"recent","title":"Transport Unit Identifier (TUID)",
     "img":"TUIDSystemDesignV2-e1627666065651.png",
     "text":"My previous investigations into the problem of trucking \u201cphantom data\u201d led to a proposal for an industry-standard Transport Unit ID (TUID). As a conversation starter, I proposed a simple method by which any shipper could create an ID that was extremely unlikely to conflict with those created by other shippers. The TUID idea, in turn, has led to many interesting possibilities to improve cooperation and interoperability among trucking industry stakeholders."},
    {"year":"2022\u20132024","era":"recent","title":"Supply Chain Data Standards",
     "img":"Standards-e1699904717833-scaled.png",
     "text":"In the aftermath of the Pandemic, global supply chain stakeholders have been doing a deep re-evaluation of SC structure, performance and transparency. I have since joined working groups for ISO 8000-119 and ASTM F49.01. The former has proposed a format for a global Transport Unit ID (TUID) that can uniquely identify any shipment, anywhere in the world. Even better, the 8000-119 TUID can be self-generated by the parties to the shipment."},
    {"year":"2022","era":"recent","title":"Canadian Grain Plaza",
     "img":"ClimbingMountain-scaled.png",
     "text":"Canadian prairie grain producers have been exporting their crops around the world for many decades. However, the system is still focused on selling and shipping bulk quantities. Even though Canada grows some of the highest quality grains in the world, Canadian farmers often get the commodity price rather than the premium price that their crops deserve. I am working with a long-time colleague on an idea to change that."},
    {"year":"2025","era":"recent","title":"DeeperPoint AI Matching",
     "img":"assets/myimages/marketforge-workflow-funnel.png",
     "text":"The initiative for selling prairie grains morphed into a focus on developing an AI-enhanced system to match remote and arms-length business interests. A system like this might consummate the deal, but it could plausibly help the parties to speed through the mating dance to decide if they want to finish up offline."},
]

ERA_CONFIG = {
    "recent":   {"label":"Recent",  "dates":"2011 \u2013 2026","order":0},
    "ipov":     {"label":"iPOV",    "dates":"1997 \u2013 2014","order":1},
    "academic": {"label":"Academic","dates":"1987 \u2013 2012","order":2},
    "origins":  {"label":"Origins", "dates":"1974 \u2013 1989","order":3},
}

def build_entry_html(e):
    img_path = e["img"] if "/" in e["img"] else f'images/about/{e["img"]}'
    return f'''                        <details class="timeline__entry">
                            <summary class="timeline__entry-header">
                                <span class="timeline__entry-year">{e["year"]}</span>
                                <span class="timeline__entry-title">{e["title"]}</span>
                                <span class="timeline__entry-chevron" aria-hidden="true">\u25b8</span>
                            </summary>
                            <div class="timeline__entry-body">
                                <figure class="timeline__figure">
                                    <img src="{img_path}" alt="{e["title"]}" loading="lazy">
                                </figure>
                                <p>{e["text"]}</p>
                            </div>
                        </details>'''

def build_era_html(era_key, entries):
    cfg = ERA_CONFIG[era_key]
    items = "\n".join(build_entry_html(e) for e in entries)
    return f'''
                <!-- {cfg["label"]} Phase -->
                <div class="timeline__item timeline__item--{era_key}">
                    <div class="timeline__header">
                        <span class="timeline__badge">{cfg["label"]}</span>
                        <span class="timeline__date">{cfg["dates"]}</span>
                    </div>
                    <div class="timeline__content">
{items}
                    </div>
                </div>'''

# Group entries by era, maintaining order
eras = {}
for e in ENTRIES:
    eras.setdefault(e["era"], []).append(e)

# Sort eras by order, entries within each era reverse-chronological
era_html_parts = []
for era_key in sorted(ERA_CONFIG.keys(), key=lambda k: ERA_CONFIG[k]["order"]):
    if era_key in eras:
        era_html_parts.append(build_era_html(era_key, reversed(eras[era_key])))

timeline_html = "\n".join(era_html_parts)

# Read the current file as template - we'll preserve intro + gantt, replace timeline
src = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history.html")
with open(src, "r", encoding="utf-8") as f:
    original = f.read()

# Find the timeline section and replace it
# Try the new marker first (from previous runs), then fall back to original
for marker in ['<!-- Full Visual Timeline with Expandable Cards -->', '<!-- Succinct Timeline -->']:
    if marker in original:
        before_idx = original.index(marker)
        break
else:
    raise ValueError("Cannot find timeline marker in history.html")
# Find the closing </section> after the timeline
section_end = original.index('</section>', before_idx)
# Include the </section> tag
after_idx = section_end + len('</section>')

new_timeline_section = f'''<!-- Full Visual Timeline with Expandable Cards -->
            <div class="timeline reveal" style="margin-top: var(--space-3xl);">
{timeline_html}
            </div>

        </div>
    </section>'''

new_html = original[:before_idx] + new_timeline_section + original[after_idx:]

# Write output
with open(src, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Generated history.html with {len(ENTRIES)} entries across {len(eras)} eras")
