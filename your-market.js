/**
 * your-market.js — the sentence box in the Home band "What about my market?" (titled "What market should exist?" until 2026-11-24).
 * Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.
 *
 * Stage 1 (live): a visitor's sentence is matched against the catalog ideas here in the
 * browser, with the word index scripts/build_idea_index.py writes (catalog/idea-index.json).
 * No model runs and nothing is sent. The sentence leaves the browser only if the visitor
 * presses "Send this idea", which posts it to the request service the demos page uses.
 *
 * Stage 2 (not live): set ANSWER_API to a service that writes a short paragraph from the
 * matches. The call and the place the paragraph lands are already here; see summarise().
 * Turning it on sends the visitor's sentence to that service, so the privacy line under
 * the box (#ym-privacy in index.html) must change in the same commit.
 *
 * stem() must stay identical to stem() in scripts/build_idea_index.py.
 */
(function () {
  "use strict";

  var INDEX_URL = "catalog/idea-index.json";
  var REQUEST_API = "https://teardown.deeperpoint.com";   // the demos page's request service
  // The service has no "idea" kind until TeardownWorkbench is redeployed with one; "ask" is
  // accepted today and reaches the owner. The note says plainly what the message is.
  var REQUEST_KIND = "ask";
  var ANSWER_API = null;      // stage 2: e.g. "https://teardown.deeperpoint.com/idea/summary"
  var CLOSE_ENOUGH = 8;       // below this best score, say that nothing in the catalog is close
  var SHOWN = 3;

  var form = document.getElementById("ym-form");
  if (!form) return;
  var input = document.getElementById("ym-input");
  var out = document.getElementById("ym-out");
  var index = null, loading = null, lastIdea = "";

  var STOP = ("a about above after again against all also am an and any are aren as at be because been before " +
    "being below between both but by can cannot could did do does doing don down during each few for " +
    "from further had has have having he her here hers him his how i if in into is it its itself just " +
    "me more most my no nor not now of off on once only or other our ours out over own same she should " +
    "so some such than that the their theirs them then there these they this those through to too " +
    "under until up very was we were what when where which while who whom why will with would you your " +
    "yours need needs want wants like get one two may might must new use used using make makes made " +
    "market markets marketplace platform match matching matches connect connecting connects find " +
    "finding people someone something thing things way ways help helps via per etc").split(" ");
  var stop = {};
  STOP.forEach(function (w) { stop[w] = true; });

  function ends(w, s) { return w.slice(-s.length) === s; }

  function stem(w) {
    if (w.length > 4 && ends(w, "ies")) return w.slice(0, -3) + "y";
    if (w.length > 5 && ends(w, "sses")) return w.slice(0, -2);
    if (w.length > 6 && ends(w, "ing")) return w.slice(0, -3);
    if (w.length > 5 && ends(w, "ed")) return w.slice(0, -2);
    if (w.length > 5 && ends(w, "ers")) return w.slice(0, -1);
    if (w.length > 4 && ends(w, "es") && !ends(w, "ses")) return w.slice(0, -2);
    if (w.length > 3 && ends(w, "s") && !ends(w, "ss") && !ends(w, "us")) return w.slice(0, -1);
    return w;
  }

  function tokens(text) {
    var seen = {}, list = [];
    (String(text).toLowerCase().replace(/’/g, "'").match(/[a-z][a-z0-9]+/g) || []).forEach(function (w) {
      if (w.length < 3 || stop[w]) return;
      var s = stem(w);
      if (!seen[s]) { seen[s] = true; list.push(s); }
    });
    return list;
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }

  function load() {
    if (!loading) {
      loading = fetch(INDEX_URL).then(function (r) {
        if (!r.ok) throw new Error("index " + r.status);
        return r.json();
      }).then(function (d) { index = d; return d; });
      loading.catch(function () { loading = null; });
    }
    return loading;
  }

  // The match itself: add up each idea's finished weights for the words in the sentence.
  function match(idea) {
    var words = tokens(idea), score = {};
    words.forEach(function (t) {
      var p = index.postings[t] || [];
      for (var i = 0; i < p.length; i += 2) score[p[i]] = (score[p[i]] || 0) + p[i + 1];
    });
    var ranked = Object.keys(score).map(function (d) { return [Number(d), score[d]]; })
      .sort(function (a, b) { return b[1] - a[1]; }).slice(0, 5);

    // Frictions: what the closest ideas lean on, plus any the visitor named outright.
    var f = {};
    ranked.forEach(function (r) {
      index.docs[r[0]].frictions.forEach(function (fi, rank) {
        // weight: rarer frictions say more about this idea than one nearly every idea shares
        f[fi] = (f[fi] || 0) + (r[1] / ranked[0][1]) * (3 - rank) * index.frictions[fi].weight;
      });
    });
    index.frictions.forEach(function (fr, fi) {
      if (words.some(function (w) { return fr.terms.indexOf(w) !== -1; })) f[fi] = (f[fi] || 0) + 4;
    });
    var frictions = Object.keys(f).map(Number).sort(function (a, b) { return f[b] - f[a]; }).slice(0, SHOWN);

    return { words: words, ideas: ranked.slice(0, SHOWN), best: ranked.length ? ranked[0][1] : 0, frictions: frictions };
  }

  function count(name) {            // usage only: the sentence is never part of the count
    try {
      if (window.goatcounter && window.goatcounter.count) {
        window.goatcounter.count({ path: "your-market/" + name, title: "Your market: " + name, event: true });
      }
    } catch (e) { /* counting is optional */ }
  }

  function render(idea, m) {
    var html = "";
    if (m.words.length < 2) {
      out.innerHTML = '<p class="ym-note">Say a little more: who has something, and who needs it?</p>';
      out.hidden = false;
      return;
    }
    var close = m.best >= CLOSE_ENOUGH;
    if (!m.ideas.length) {
      html += '<p class="ym-note"><strong>Nothing in the catalog shares your words.</strong> ' +
        "That can mean the idea is new to us. You can send it, or " +
        '<a href="catalog/index.html">browse the catalog</a> by sector.</p>';
    } else {
      html += "<h3>" + (close ? "The closest ideas in the catalog" : "Nothing close yet. The nearest we have") + "</h3>" +
        '<ul class="ym-ideas">' + m.ideas.map(function (r) {
          var d = index.docs[r[0]];
          return '<li><a href="catalog/' + encodeURIComponent(d.id) + '.html"><b>' + esc(d.title) + "</b>" +
            "<span>" + esc(d.sector) + "</span><p>" + esc(d.summary) + "</p></a></li>";
        }).join("") + "</ul>";
      if (m.frictions.length) {
        html += "<h3>What tends to stand in the way of markets like these</h3>" +
          '<ul class="ym-frictions">' + m.frictions.map(function (fi) {
            var fr = index.frictions[fi];
            return '<li><a href="cards/index.html#' + fr.slug + '"><b>' + esc(fr.title) + "</b>" +
              "<p>" + esc(fr.definition) + "</p></a></li>";
          }).join("") + "</ul>";
      }
      // Say the near-universal friction once, in words, when it is not already in the list.
      index.frictions.forEach(function (fr, fi) {
        if (fr.share >= 0.75 && m.frictions.indexOf(fi) === -1) {
          html += '<p class="ym-caveat">Nearly every idea in the catalog (' + Math.round(fr.share * 100) +
            '%) also faces <a href="cards/index.html#' + fr.slug + '">' + esc(fr.title) + "</a>: " +
            esc(fr.definition.charAt(0).toLowerCase() + fr.definition.slice(1)) + "</p>";
        }
      });
      html += '<div id="ym-summary" class="ym-summary" hidden></div>';
      html += '<p class="ym-caveat">This is a word match against ' + index.count + " catalog ideas, none of them built. " +
        "It says what markets like this one usually face, not what yours does. A " +
        '<a href="marketmaps.html">MarketMap</a> is the closer look: it reads a company&rsquo;s own material.</p>';
    }
    html += '<div class="ym-next">' +
      '<button type="button" class="btn btn--primary" id="ym-send-open">Send this idea to DeeperPoint &rarr;</button>' +
      '<a class="btn btn--outline" href="demos.html#marketmap">Ask for a MarketMap code &rarr;</a></div>' +
      '<form id="ym-send" class="ym-send" hidden novalidate>' +
      "<p>A person reads these. You will hear back by email if there is something useful to say.</p>" +
      '<label for="ym-name">Your name</label><input id="ym-name" name="name" type="text" autocomplete="name" maxlength="80" required>' +
      '<label for="ym-email">Email</label><input id="ym-email" name="email" type="email" autocomplete="email" maxlength="120" required>' +
      '<label class="ym-check"><input type="checkbox" name="catalog"> DeeperPoint may add this idea to the public catalog, without my name</label>' +
      '<div class="ym-trap" aria-hidden="true"><label for="ym-website">Leave this empty</label>' +
      '<input id="ym-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>' +
      '<div id="ym-check"></div>' +
      '<div class="ym-msg" id="ym-msg" role="status" hidden></div>' +
      '<button type="submit" class="btn btn--primary" id="ym-send-go">Send &rarr;</button>' +
      '<p class="ym-fine">Sent: your sentence, your name and your email. Used only to answer you, and to add the idea to the catalog if you ticked the box.</p>' +
      "</form>";
    out.innerHTML = html;
    out.hidden = false;
    document.getElementById("ym-send-open").addEventListener("click", openSend);
    document.getElementById("ym-send").addEventListener("submit", send);
    if (m.ideas.length) summarise(idea, m);
  }

  // Stage 2. Off while ANSWER_API is null. The service gets the sentence and what was matched,
  // and returns { text: "..." }: three or four sentences written only from those ideas and cards.
  function summarise(idea, m) {
    if (!ANSWER_API) return;
    var box = document.getElementById("ym-summary");
    var body = {
      idea: idea,
      ideas: m.ideas.map(function (r) { return index.docs[r[0]].id; }),
      frictions: m.frictions.map(function (fi) { return index.frictions[fi].slug; })
    };
    fetch(ANSWER_API, { method: "POST", headers: { "Content-Type": "text/plain" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d || !d.text || idea !== lastIdea) return;
        box.innerHTML = '<span class="ym-summary__label">Written by an AI model from the ideas above</span><p>' + esc(d.text) + "</p>";
        box.hidden = false;
      })
      .catch(function () { /* the matches stand on their own */ });
  }

  // ── Sending the idea: the only path by which the sentence leaves the browser ──
  var config = null, widget = null;
  var SAID = {
    received: "Thank you. Your idea has been sent.",
    limit: "There have been several messages from this connection today. Please try again tomorrow.",
    check: "The bot check did not pass. Please try again.",
    invalid: "Please give your name and a valid email address.",
    network: 'The message did not get through. Please try again, or write to us from the <a href="about.html">About page</a>.'
  };

  function say(key, ok) {
    var msg = document.getElementById("ym-msg");
    msg.innerHTML = SAID[key] || SAID.network;
    msg.className = "ym-msg" + (ok ? " ym-msg--ok" : "");
    msg.hidden = false;
  }

  function botCheck(siteKey) {
    if (!siteKey || widget !== null) return;
    widget = false;
    var s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    s.onload = function () { widget = window.turnstile.render("#ym-check", { sitekey: siteKey, theme: "dark" }); };
    document.head.appendChild(s);
  }

  function openSend() {
    var f = document.getElementById("ym-send");
    f.hidden = false;
    document.getElementById("ym-send-open").hidden = true;
    document.getElementById("ym-name").focus();
    widget = null;                    // the form was rebuilt, so the check is drawn afresh
    if (config) return botCheck(config.turnstile_site_key);
    fetch(REQUEST_API + "/invite/config").then(function (r) { return r.json(); })
      .then(function (c) { config = c; botCheck(c.turnstile_site_key); })
      .catch(function () {});
  }

  function send(e) {
    e.preventDefault();
    var f = e.target, go = document.getElementById("ym-send-go");
    var name = f.elements.name.value.trim(), email = f.elements.email.value.trim();
    if (!name || !/^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$/.test(email)) return say("invalid", false);
    // The service keeps 300 characters of note; the box allows 200, so the label always fits.
    var note = "MARKET IDEA from the Home page (catalog: " + (f.elements.catalog.checked ? "yes" : "no") + "): " + lastIdea;
    var body = { demo: REQUEST_KIND, name: name, email: email, note: note.slice(0, 300), website: f.elements.website.value };
    var checked = typeof widget === "string" && window.turnstile;
    if (checked) body.turnstile = window.turnstile.getResponse(widget) || "";
    go.disabled = true;
    fetch(REQUEST_API + "/invite/request", { method: "POST", headers: { "Content-Type": "text/plain" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var done = d.outcome === "received" || d.outcome === "sent";
        say(done ? "received" : d.outcome, done);
        if (done) { go.hidden = true; count("sent"); }
        else { go.disabled = false; if (checked) window.turnstile.reset(widget); }
      })
      .catch(function () { say("network", false); go.disabled = false; });
  }

  // Fetch the index when the visitor shows interest, not on every page view.
  input.addEventListener("focus", function () { load().catch(function () {}); }, { once: true });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var idea = input.value.trim().replace(/\s+/g, " ");
    if (!idea) return input.focus();
    lastIdea = idea;
    out.hidden = false;
    out.innerHTML = '<p class="ym-note">Looking through the catalog&hellip;</p>';
    load().then(function () {
      var m = match(idea);
      render(idea, m);
      count(m.ideas.length ? (m.best >= CLOSE_ENOUGH ? "matched" : "weak") : "none");
    }).catch(function () {
      out.innerHTML = '<p class="ym-note">The catalog index did not load. You can ' +
        '<a href="catalog/index.html">browse the catalog</a> instead.</p>';
    });
  });
})();
