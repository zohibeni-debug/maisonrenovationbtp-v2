/* Artisan Druart : menu, diagnostic de façade, estimateur, nuancier, avant/après et formulaire de devis. */
(function () {
  "use strict";

  var PHONE = "__PHONE__";
  var WHATSAPP = "__WHATSAPP__";
  var doc = document;

  function $(s, r) { return (r || doc).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); }
  function fmt(v) {
    v = Math.round(v / 50) * 50;
    return v.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "\u00a0") + " €";
  }

  // Menu mobile
  var header = $("[data-header]");
  var toggle = $(".menu-btn");
  function setMenu(open) {
    header.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    doc.body.classList.toggle("no-scroll", open);
  }
  if (header && toggle) {
    toggle.addEventListener("click", function () { setMenu(!header.classList.contains("open")); });
    window.matchMedia("(min-width: 1100px)").addEventListener("change", function (m) { if (m.matches) setMenu(false); });
  }

  // Sous-menus : un seul ouvert, fermeture au clic extérieur et avec Échap
  var subs = $$(".sub");
  subs.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open) subs.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });
  doc.addEventListener("click", function (e) {
    if (window.innerWidth < 1100) return;
    subs.forEach(function (d) { if (d.open && !d.contains(e.target)) d.open = false; });
  });
  doc.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    subs.forEach(function (d) { if (d.open) { d.open = false; $("summary", d).focus(); } });
    if (header && header.classList.contains("open")) { setMenu(false); toggle.focus(); }
  });

  // Barre d'appel mobile et en-tête plein au défilement
  var callbar = $("[data-callbar]");
  var home = doc.body.classList.contains("p-home");
  var tick = false;
  function onScroll() {
    if (tick) return;
    tick = true;
    window.requestAnimationFrame(function () {
      var y = window.scrollY || window.pageYOffset;
      if (callbar) callbar.classList.toggle("show", y > 420);
      if (home && header) header.classList.toggle("solid", y > 60);
      tick = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Vidéo de fond : chargée seulement si l'utilisateur accepte les animations et n'économise pas ses données
  var vid = $("[data-hero-video]");
  if (vid) {
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var save = navigator.connection && navigator.connection.saveData;
    if (!reduce && !save) {
      $$("source[data-src]", vid).forEach(function (s) { s.src = s.getAttribute("data-src"); });
      vid.load();
      var p = vid.play();
      if (p && p.catch) p.catch(function () {});
    }
  }

  // Diagnostic de façade (onglets)
  var diag = $("[data-diag]");
  if (diag) {
    var tabs = $$("[role=tab]", diag);
    var select = function (btn, focus) {
      var key = btn.getAttribute("data-key");
      tabs.forEach(function (t) {
        var on = t === btn;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
      });
      $$("[data-tile]", diag).forEach(function (s) {
        var on = s.getAttribute("data-tile") === key;
        s.hidden = !on;
        s.classList.toggle("is-in", on);
      });
      $$("[data-panel]", diag).forEach(function (p) { p.hidden = p.getAttribute("data-panel") !== key; });
      if (focus) btn.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var k = e.key, n = null;
        if (k === "ArrowDown" || k === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        if (k === "ArrowUp" || k === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (k === "Home") n = tabs[0];
        if (k === "End") n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
  }

  // Estimateur de budget
  var est = $("[data-estim]");
  if (est) {
    var range = $("input[type=range]", est), outS = $("[data-surf]", est), out = $("[data-out]", est);
    var calc = function () {
      var s = Number(range.value), lo = 0, hi = 0, n = 0;
      $$("input[type=checkbox]", est).forEach(function (c) {
        if (c.checked) { lo += Number(c.getAttribute("data-min")); hi += Number(c.getAttribute("data-max")); n++; }
      });
      outS.textContent = s + " m²";
      out.textContent = n ? fmt(lo * s) + " à " + fmt(hi * s) : "Cochez au moins un travail";
    };
    est.addEventListener("input", calc);
    est.addEventListener("change", calc);
    calc();
  }

  // Nuancier
  var nu = $("[data-nuancier]");
  if (nu) {
    $$(".sw", nu).forEach(function (b) {
      b.addEventListener("click", function () {
        nu.style.setProperty("--wall", b.getAttribute("data-sw"));
        $$(".sw", nu).forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      });
    });
  }

  // Avant / après
  $$("[data-ba]").forEach(function (f) {
    var r = $("input", f);
    r.addEventListener("input", function () { f.style.setProperty("--pos", r.value + "%"); });
  });

  // Formulaire de devis
  var form = doc.getElementById("devis-form");
  if (!form) return;
  var status = doc.getElementById("form-status");

  function el(tag, attrs, text) {
    var n = doc.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text) n.textContent = text;
    return n;
  }
  function show(kind, nodes) {
    status.className = "form-status " + kind;
    status.textContent = "";
    nodes.forEach(function (n) { status.appendChild(n); });
    status.setAttribute("tabindex", "-1");
    status.focus();
  }
  function summary(d) {
    return "Demande de devis (site maisonrenovationbtp.fr)\n" +
      "Nom : " + d.nom + "\nTéléphone : " + d.telephone + "\n" +
      (d.email ? "Email : " + d.email + "\n" : "") +
      "Commune : " + d.commune + "\nTravaux : " + d.type + "\nRappel : " + d.rappel + "\n\n" + d.message;
  }
  function fallback(d) {
    var text = summary(d);
    var actions = el("div", { "class": "fallback-actions" });
    actions.appendChild(el("a", { "class": "btn btn-primary", href: "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(text), rel: "noopener" }, "Envoyer sur WhatsApp"));
    actions.appendChild(el("a", { "class": "btn btn-ghost", href: "sms:" + PHONE + "?&body=" + encodeURIComponent(text) }, "Envoyer par SMS"));
    actions.appendChild(el("a", { "class": "btn btn-ghost", href: "tel:" + PHONE }, "Appeler"));
    show("err", [el("p", {}, "L'envoi par le site n'a pas abouti. Votre demande est prête : envoyez-la par WhatsApp ou par SMS, ou appelez-nous."), actions]);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var first = null;
    $$("[required]", form).forEach(function (f) {
      var ok = f.type === "checkbox" ? f.checked : f.value.trim() !== "" && f.checkValidity();
      f.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok && !first) first = f;
    });
    if (first) {
      show("err", [el("p", {}, "Complétez les champs signalés en rouge.")]);
      first.focus();
      return;
    }
    var rap = $("input[name=rappel]:checked", form);
    var d = {
      nom: form.elements.nom.value.trim(),
      telephone: form.elements.telephone.value.trim(),
      email: form.elements.email ? form.elements.email.value.trim() : "",
      commune: form.elements.commune.value.trim(),
      type: form.elements.type.value,
      message: form.elements.message.value.trim(),
      rappel: rap ? rap.value : "Indifférent",
      site_web: form.elements.site_web.value,
      consentement: form.elements.consentement.checked,
      page: location.pathname
    };
    var button = $("button[type=submit]", form);
    var label = $("span", button);
    button.disabled = true;
    label.textContent = "Envoi en cours…";
    fetch("/api/devis", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(d) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; }); })
      .then(function (res) {
        if (res.status === 200 && res.body.ok) {
          form.reset();
          show("ok", [el("p", {}, "Demande envoyée. Nous vous rappelons pour convenir d'une visite.")]);
        } else if (res.status === 400 && res.body.error) {
          show("err", [el("p", {}, res.body.error)]);
        } else {
          fallback(d);
        }
      })
      .catch(function () { fallback(d); })
      .then(function () { button.disabled = false; label.textContent = "Envoyer ma demande"; });
  });
})();
