/* daya_na990 — timeline unique des 15 scènes (GSAP, seek-safe).
 * Structure reprise du gabarit 4roues-parcours, contenu : la boutique BIKINI SHOP (@daya_na990 sur TikTok).
 *
 * Toutes les heures sont en secondes, calées sur l'analyse (±0,25 s).
 * Chaque scène est une <section class="clip"> dont la fenêtre data-start/data-duration
 * déborde un peu sur ses voisines pour laisser la place aux transitions.
 * On anime toujours un enfant (.cam, .center…), jamais la section elle-même.
 * index.html appelle buildDaya() et enregistre la timeline sur window.__timelines.
 */
window.buildDaya = function () {
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => Array.from(document.querySelectorAll(s));
  const SVGNS = "http://www.w3.org/2000/svg";

  /* ---------- construction du DOM (synchrone, déterministe) ---------- */

  // Logo : une seule source (template), clonée dans chaque emplacement [data-logo]
  const logoTpl = $("#logo-tpl");
  $$("[data-logo]").forEach((slot) => slot.appendChild(logoTpl.content.cloneNode(true)));

  // Texte découpé lettre par lettre pour les apparitions depuis le flou
  $$(".split").forEach((el) => {
    const txt = el.textContent;
    el.textContent = "";
    for (const c of txt) {
      const s = document.createElement("span");
      s.className = "ch";
      s.textContent = c;
      el.appendChild(s);
    }
  });

  // Citation de l'avis : découpage mot par mot (le dernier groupe reste rouge)
  (function splitWords(el) {
    const parts = [];
    el.childNodes.forEach((n) => {
      const red = n.nodeType === 1;
      n.textContent
        .split(/\s+/)
        .filter(Boolean)
        .forEach((w) => parts.push({ w, red }));
    });
    el.textContent = "";
    parts.forEach((p, i) => {
      const s = document.createElement("span");
      s.className = "word" + (p.red ? " red" : "");
      s.textContent = p.w;
      el.appendChild(s);
      if (i < parts.length - 1) el.appendChild(document.createTextNode(" "));
    });
  })($("#s12-quote"));

  // Étoiles (contour gris + remplissage jaune qui s'agrandit)
  const STAR = "M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.4l-5.9 3.2 1.3-6.6-4.9-4.6 6.6-.8z";
  for (let i = 0; i < 5; i++) {
    const d = document.createElement("div");
    d.className = "star";
    d.innerHTML =
      `<svg viewBox="0 0 24 24" width="58" height="58"><path d="${STAR}" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="1.4"/></svg>` +
      `<svg class="star-fill" viewBox="0 0 24 24" width="58" height="58"><path d="${STAR}" fill="#ffc531"/></svg>`;
    $("#s12-stars").appendChild(d);
  }

  // Vue éclatée (scène 8) : les couches du DM se chevauchent volontairement en perspective
  $$("#s7-stack *").forEach((n) => n.setAttribute("data-layout-allow-overlap", ""));

  // Téléphone de la scène 10 : copie réduite de l'écran profil (sans les id)
  const mini = $("#s4-profile").cloneNode(true);
  mini.removeAttribute("id");
  mini.querySelectorAll("[id]").forEach((n) => n.removeAttribute("id"));
  $("#s10-mini").appendChild(mini);

  // Tuiles-icônes flottantes autour du téléphone (scène 11)
  const IC = {
    bag: '<path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 016 0v2"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    heart: '<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z"/>',
    box: '<path d="M3 8l9-4 9 4v9l-9 4-9-4z"/><path d="M3 8l9 4 9-4M12 12v9"/>',
    truck: '<path d="M2 7h11v9H2zM13 10h4l3 3v3h-7z"/><circle cx="6" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
    star: `<path d="${STAR}"/>`,
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/>',
    card: '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h4"/>',
  };
  const TILES = [
    // [classe, icône, x, y, profondeur z, rotation]
    ["r", "bag", 90, 640, 120, -12],
    ["g", "card", 830, 620, -60, 10],
    ["r", "check", 820, 900, 80, 8],
    ["g", "box", 120, 1150, -40, -6],
    ["g", "star", 860, 1430, 40, 12],
    ["r", "heart", 150, 1700, 60, -10],
    ["g", "truck", 800, 1680, -80, 6],
    ["g", "sun", 60, 400, -120, 8],
  ];
  TILES.forEach(([cls, ic, x, y], i) => {
    const t = document.createElement("div");
    t.className = "ftile " + cls;
    t.id = "s11-tile-" + i;
    t.style.left = x + "px";
    t.style.top = y + "px";
    t.innerHTML = `<svg width="78" height="78" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${IC[ic]}</svg>`;
    $("#s11-tiles").appendChild(t);
  });

  // Bulles blanches floues (fermeture de la scène 11)
  const BUB = [
    [540, 960, 520],
    [200, 520, 360],
    [880, 640, 400],
    [260, 1400, 440],
    [860, 1360, 380],
    [540, 1780, 420],
    [540, 200, 380],
  ];
  BUB.forEach(([x, y, r], i) => {
    const b = document.createElement("div");
    b.className = "wbub";
    b.id = "s11-bub-" + i;
    b.style.left = x - r + "px";
    b.style.top = y - r + "px";
    b.style.width = 2 * r + "px";
    b.style.height = 2 * r + "px";
    $("#s11-bubbles").appendChild(b);
  });

  // Étincelles de l'explosion (scène 14) : 18 traits répartis régulièrement
  for (let i = 0; i < 18; i++) {
    const s = document.createElement("div");
    s.className = "spark";
    s.style.rotate = (i * 360) / 18 + (i % 2 ? 7 : 0) + "deg";
    $("#s14-burst").appendChild(s);
  }

  // Garage isométrique en CSS 3D (scène 12) : sol = plan XY, hauteur = Z
  const iso = $("#s12-iso");
  function face(parent, w, h, bg, transform) {
    const f = document.createElement("div");
    f.className = "face";
    f.style.width = w + "px";
    f.style.height = h + "px";
    f.style.background = bg;
    f.style.transformOrigin = "0 0";
    f.style.transform = transform;
    parent.appendChild(f);
    return f;
  }
  function box(x, y, z, w, d, h, c) {
    const top = face(iso, w, d, c.top, `translate3d(${x}px,${y}px,${z + h}px)`);
    const south = face(iso, w, h, c.south, `translate3d(${x}px,${y + d}px,${z + h}px) rotateX(-90deg)`);
    const north = face(iso, w, h, c.north || c.south, `translate3d(${x + w}px,${y}px,${z + h}px) rotateZ(180deg) rotateX(-90deg)`);
    const east = face(iso, d, h, c.east, `translate3d(${x + w}px,${y + d}px,${z + h}px) rotateZ(-90deg) rotateX(-90deg)`);
    const west = face(iso, d, h, c.west || c.east, `translate3d(${x}px,${y}px,${z + h}px) rotateZ(90deg) rotateX(-90deg)`);
    return { top, south, north, east, west };
  }
  const WALL = { top: "#fff4e8", south: "#ffe3d0", east: "#f3c9b4", west: "#f6d3c0" };
  // socle
  const slab = box(0, 0, 0, 700, 700, 34, { top: "#fffaf3", south: "#f1e4d2", east: "#e2cfb6" });
  // sable, mer et terrasse dessinés sur le dessus du socle
  slab.top.innerHTML =
    '<div style="position:absolute;left:20px;top:20px;width:110px;height:660px;border-radius:18px;background:#a9d98c"></div>' +
    '<div style="position:absolute;left:150px;top:400px;width:530px;height:280px;border-radius:14px;background:#f3d3a4"></div>' +
    '<div style="position:absolute;left:150px;top:560px;width:530px;height:120px;border-radius:0 0 14px 14px;background:#3ccfcf"></div>' +
    [0, 1, 2].map((i) => `<div style="position:absolute;left:${210 + i * 150}px;top:440px;width:70px;height:70px;border-radius:50%;background:${["#ff4f70", "#ffc93c", "#16a6a0"][i]}"></div>`).join("");
  // boutique
  const bld = box(150, 70, 34, 400, 280, 200, WALL);
  // toit corail
  box(140, 60, 234, 420, 300, 18, { top: "#ff6f61", south: "#e2574a", east: "#c9473c" });
  // façade sud : enseigne « BIKINI SHOP » + vitrine
  bld.south.innerHTML =
    '<div style="position:absolute;left:50px;top:18px;width:300px;height:48px;border-radius:24px;background:#ff4f70;display:flex;align-items:center;justify-content:center;font:900 26px Unbounded, sans-serif;letter-spacing:.02em;color:#fff">BIKINI SHOP</div>' +
    '<div style="position:absolute;left:60px;top:80px;width:280px;height:120px;border-radius:8px 8px 0 0;background:#35557c;border:6px solid #fff4e8"></div>';
  // façade ouest (côté caméra) : trois fenêtres
  bld.west.innerHTML = [0, 1, 2]
    .map((i) => `<div style="position:absolute;left:${28 + i * 84}px;top:40px;width:62px;height:100px;border-radius:31px 31px 6px 6px;background:#d3f0ea"></div>`)
    .join("");
  // palmiers stylisés (tronc + touffe)
  [
    [50, 80],
    [50, 330],
    [50, 580],
  ].forEach(([x, y]) => {
    box(x + 16, y + 16, 34, 16, 16, 90, { top: "#a97b50", south: "#a97b50", east: "#8a6240" });
    box(x, y, 124, 48, 48, 26, { top: "#2f9e6e", south: "#1f7a55", east: "#1a6a4a" });
  });

  /* ---------- helpers d'animation ---------- */

  const tl = gsap.timeline({ paused: true });

  // entrée « depuis le flou » : blur + léger zoom, net à l'arrivée
  function blurIn(targets, at, o = {}) {
    tl.fromTo(
      targets,
      { opacity: 0, filter: `blur(${o.blur ?? 18}px)`, scale: o.scale ?? 1.25, y: o.y ?? 0 },
      { opacity: 1, filter: "blur(0px)", scale: 1, y: 0, duration: o.dur ?? 0.45, ease: o.ease ?? "power3.out", stagger: o.stagger ?? 0 },
      at,
    );
  }
  // sortie avec flou de mouvement (whip) : rotation 3D + blur qui culmine
  function whipOut(target, at, o = {}) {
    tl.to(
      target,
      {
        opacity: 0,
        filter: `blur(${o.blur ?? 26}px)`,
        rotationX: o.rx ?? 0,
        rotationY: o.ry ?? 0,
        scale: o.scale ?? 1.4,
        x: o.x ?? 0,
        y: o.y ?? 0,
        duration: o.dur ?? 0.3,
        ease: "power2.in",
      },
      at,
    );
  }
  // coche qui se dessine
  function drawCheck(path, at) {
    tl.fromTo(path, { strokeDasharray: 24, strokeDashoffset: 24 }, { strokeDashoffset: 0, duration: 0.25, ease: "power2.out" }, at);
  }
  // nombre qui défile (onUpdate = seek-safe, la valeur dépend seulement du temps)
  const fmt = (n) => Math.round(n).toLocaleString("fr-FR").replace(/\s/g, " ");
  function count(el, from, to, at, dur, render = fmt) {
    const o = { v: from };
    tl.fromTo(o, { v: from }, { v: to, duration: dur, ease: "power2.out", onUpdate: () => (el.textContent = render(o.v)) }, at);
  }
  // texte qui se tape
  function typeText(el, base, full, at, dur) {
    const o = { n: base.length };
    tl.fromTo(
      o,
      { n: base.length },
      { n: full.length, duration: dur, ease: "none", onUpdate: () => (el.textContent = full.slice(0, Math.round(o.n))) },
      at,
    );
  }

  /* ================= S1 · point rouge (0 → 1) ================= */
  // frame 0 = dernière frame de la vidéo (boucle) : losange 45°, halo au repos
  tl.set("#s1-dot", { rotation: 45, scale: 1 }, 0);
  tl.fromTo("#s1-halo", { scale: 0.35, opacity: 0.7 }, { scale: 0.6, opacity: 1, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 3 }, 0);
  tl.to("#s1-dot", { rotation: 45 + 70, scale: 3.2, duration: 0.95, ease: "power2.in" }, 0.05);
  tl.to("#s1-halo", { scale: 1.6, duration: 0.35, ease: "power2.in" }, 0.75);
  tl.to("#s1-cam", { opacity: 0, filter: "blur(10px)", duration: 0.15 }, 1.0);

  /* ================= S2 · logo néon (1 → 2) ================= */
  tl.fromTo("#s2-flash", { scale: 0.2, opacity: 1 }, { scale: 1.3, opacity: 0, duration: 0.6, ease: "power2.out" }, 0.95);
  tl.fromTo("#s2-logo", { opacity: 0, scale: 0.6, filter: "blur(20px) brightness(3)" }, { opacity: 1, scale: 1, filter: "blur(0px) brightness(1)", duration: 0.45, ease: "expo.out" }, 0.98);
  // petit grésillement néon
  tl.to("#s2-logo", { opacity: 0.55, duration: 0.04, yoyo: true, repeat: 3, ease: "none" }, 1.3);
  tl.fromTo("#s2-ring-c", { strokeDasharray: 2702, strokeDashoffset: 2702, rotation: -90, transformOrigin: "50% 50%" }, { strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut" }, 1.5);
  tl.to("#s2-logo", { scale: 1.04, duration: 0.5, ease: "sine.inOut" }, 1.45);
  whipOut("#s2-cam", 1.95, { scale: 0.6, blur: 22, dur: 0.28 });

  /* ================= S3 · recherche Instagram (2 → 3.5) ================= */
  tl.fromTo("#s3-cam", { rotationX: 32, rotationY: -22, rotationZ: 6, scale: 0.78, y: 160, filter: "blur(16px)", opacity: 0 }, { rotationX: 14, rotationY: -10, rotationZ: 2, scale: 0.9, y: 40, filter: "blur(0px)", opacity: 1, duration: 0.4, ease: "power3.out" }, 2.0);
  tl.to("#s3-cam", { rotationX: 0, rotationY: 0, rotationZ: 0, scale: 1, y: 0, duration: 1.1, ease: "power2.inOut" }, 2.35);
  tl.fromTo("#s3-caret", { opacity: 1 }, { opacity: 0, duration: 0.18, ease: "steps(1)", yoyo: true, repeat: 7 }, 2.0);
  tl.set("#s3-ph", { display: "none" }, 2.5);
  typeText($("#s3-q"), "", "daya_na990", 2.5, 0.42);
  tl.to("#s3-recent", { opacity: 0, y: -20, duration: 0.15 }, 2.9);
  tl.set("#s3-recent", { display: "none" }, 3.05);
  tl.fromTo("#s3-results", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out", immediateRender: true }, 3.05);
  tl.fromTo("#s3-result", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: "power2.out" }, 3.12);
  // zoom vers l'avatar du résultat
  tl.to("#s3-cam", { scale: 2.6, x: 640, y: 120, filter: "blur(14px)", opacity: 0, duration: 0.32, ease: "power3.in", transformOrigin: "16% 40%" }, 3.42);

  /* ================= S4 · profil (3.5 → 5) ================= */
  tl.fromTo("#s4-cam", { scale: 1.5, filter: "blur(14px)", opacity: 0, transformOrigin: "50% 18%" }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.4, ease: "power3.out" }, 3.47);
  tl.fromTo("#s4-screen .prof-av", { scale: 1.35 }, { scale: 1, duration: 0.5, ease: "back.out(2)" }, 3.47);
  // compteurs au format TikTok : « 2368 », « 14.5K »
  const plain = (v) => String(Math.round(v));
  const kUp = (v) => (v / 1000).toFixed(1) + "K";
  $$("#s4-screen .cnt").forEach((el, i) => {
    const a = +el.dataset.from;
    const b = +el.dataset.to;
    const render = el.dataset.format === "K" ? kUp : el.dataset.format === "plain" ? plain : fmt;
    count(el, 0, a, 3.6 + i * 0.05, 0.45, render);
    if (b !== a) count(el, a, b, 4.15, 0.55, render);
  });
  tl.fromTo("#s4-screen .bio > div", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.25, stagger: 0.05, ease: "power2.out" }, 3.7);
  tl.fromTo("#s4-screen .btn", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.25, stagger: 0.06, ease: "back.out(2)" }, 3.95);
  tl.fromTo(["#s4-gtabs", "#s4-grid"], { opacity: 0, y: 240 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 4.45);

  /* ================= S5 · scroll de la grille (5 → 6) ================= */
  tl.to("#s4-cam", { rotationX: 18, rotationZ: -3, scale: 0.94, duration: 0.35, ease: "power2.in" }, 5.0);
  tl.to("#s4-profile", { y: -1060, duration: 0.65, ease: "power3.inOut" }, 5.0);
  tl.to("#s4-cam", { filter: "blur(7px)", duration: 0.3, ease: "power2.in" }, 5.0);
  tl.to("#s4-cam", { filter: "blur(0px)", rotationX: 0, rotationZ: 0, scale: 1, duration: 0.35, ease: "power2.out" }, 5.32);
  // la tuile Boxster se détache
  tl.fromTo("#s5-tile-ring", { opacity: 0 }, { opacity: 1, duration: 0.15 }, 5.55);
  tl.fromTo("#s5-tile", { scale: 1, zIndex: 0 }, { scale: 1.18, zIndex: 5, z: 120, boxShadow: "0 30px 60px rgba(0,0,0,.8)", duration: 0.3, ease: "back.out(2)" }, 5.6);
  tl.to(["#s4-grid .tile:not(#s5-tile)", "#s4-gtabs"], { opacity: 0.25, filter: "blur(4px)", duration: 0.3 }, 5.65);
  tl.to("#s4-cam", { opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power2.in" }, 5.95);

  /* ================= S6 · reel + vues (6 → 8) ================= */
  // la carte part de la position de la tuile (bas à droite de la grille) et grandit
  tl.fromTo("#s6-card", { x: 260, y: 220, scale: 0.36, rotationX: 12, borderRadius: 120, filter: "blur(6px)" }, { x: 0, y: 0, scale: 1, rotationX: 0, borderRadius: 56, filter: "blur(0px)", duration: 0.55, ease: "power3.inOut" }, 5.78);
  tl.fromTo("#s6-media img", { scale: 1.0 }, { scale: 1.18, duration: 2.2, ease: "none" }, 5.8);
  tl.fromTo("#s6-progress", { scaleX: 0 }, { scaleX: 1, duration: 2.1, ease: "none" }, 6.0);
  tl.fromTo("#s6-card .reel-cap", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, 6.25);
  blurIn("#s6-views .pill", 6.35, { scale: 0.7, dur: 0.35 });
  // vraies vues de la vidéo mise en avant (2562 sur TikTok)
  count($("#s6-count"), 0, 1280, 6.7, 0.5, plain);
  count($("#s6-count"), 1280, 2562, 7.25, 0.5, plain);
  tl.fromTo("#s6-views .pill", { scale: 1 }, { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, ease: "power1.out", immediateRender: false }, 7.2);
  // push-in caméra
  tl.to("#s6-cam", { scale: 1.1, duration: 1.6, ease: "sine.inOut" }, 6.3);
  tl.to("#s6-cam", { scale: 1.35, opacity: 0, filter: "blur(16px)", duration: 0.3, ease: "power2.in" }, 7.9);

  /* ================= S7 · message privé (8 → 9.5) ================= */
  // filtre/opacité sur la caméra, pas sur la pile : un filter aplatirait le preserve-3d
  tl.fromTo("#s7-cam", { opacity: 0, filter: "blur(14px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }, 7.8);
  tl.fromTo("#s7-stack", { scale: 0.86 }, { scale: 1, duration: 0.4, ease: "power3.out" }, 7.8);
  tl.fromTo("#s7-header .dm-card", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3 }, 8.0);
  tl.fromTo("#s7-header .stamp", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 8.15);
  [
    ["#s7-in", 8.3],
    ["#s7-photo", 8.6],
    ["#s7-out", 8.95],
  ].forEach(([sel, at]) => tl.fromTo(sel, { opacity: 0, y: 60, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, at));
  typeText($("#s7-out-txt"), "Oui ! Dispo", "Oui ! Dispo en M, je te l'emballe ?", 9.12, 0.3);

  /* ================= S8 · vue éclatée + checklist (9.5 → 11.5) ================= */
  tl.to("#s7-stack", { rotationX: 56, rotationZ: -36, scale: 0.55, y: 70, duration: 0.7, ease: "power3.inOut" }, 9.5);
  [
    ["#s7-bg", 0],
    ["#s7-input", 60],
    ["#s7-out", 140],
    ["#s7-photo", 220],
    ["#s7-in", 300],
    ["#s7-header", 380],
  ].forEach(([sel, z], i) => tl.to(sel, { z, duration: 0.6, ease: "power3.out" }, 9.65 + i * 0.03));
  tl.to("#s7-stack .layer:not(#s7-bg)", { boxShadow: "0 0 0 2px rgba(255,255,255,.22)", duration: 0.4 }, 9.7);
  tl.to(["#s7-bg", "#s7-header"], { backgroundColor: "rgba(255,255,255,.07)", duration: 0.4 }, 9.7);
  tl.fromTo("#s8-car", { y: -700, opacity: 0, filter: "blur(12px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.55, ease: "power3.out" }, 10.1);
  tl.fromTo("#s8-plats .plat", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, stagger: 0.08, ease: "back.out(2.2)" }, 10.35);
  $$("#s8-list .chip").forEach((chip, i) => {
    const at = 10.55 + i * 0.3;
    blurIn(chip, at, { scale: 0.85, y: 40, dur: 0.35 });
    tl.fromTo(chip.querySelector(".check"), { scale: 0 }, { scale: 1, duration: 0.25, ease: "back.out(3)" }, at + 0.2);
    drawCheck(chip.querySelector(".ck"), at + 0.28);
  });
  tl.to("#s7-cam", { scale: 1.08, duration: 1.4, ease: "sine.inOut" }, 10.1);

  /* ================= S9 · plan cinéma 911 (11.5 → 14) ================= */
  tl.fromTo("#s9-media", { scale: 1.0, transformOrigin: "50% 62%" }, { scale: 1.5, duration: 2.5, ease: "power1.in" }, 11.5);
  tl.fromTo("#s9-cam", { opacity: 0 }, { opacity: 1, duration: 0.12 }, 11.5);
  tl.to("#s9-media", { filter: "blur(9px)", duration: 0.25 }, 13.4);
  tl.fromTo("#s9-plate", { x: 900, rotationY: -55, rotationX: 8, opacity: 0, filter: "blur(18px)" }, { x: 0, rotationY: -18, rotationX: 6, opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }, 13.45);
  tl.to("#s9-plate", { rotationY: -10, duration: 0.25, ease: "sine.out" }, 13.8);
  tl.to(["#s9-cam", "#s9-plate"], { opacity: 0, duration: 0.12 }, 13.92);

  /* ================= S10 · révélation du téléphone (14 → 15) ================= */
  tl.set("#s10-mini", { scale: 374 / 940 }, 0);
  tl.fromTo("#s10-phone", { scale: 0.18, opacity: 0, y: 140 }, { scale: 0.45, opacity: 1, y: 140, duration: 0.3, ease: "back.out(2)" }, 14.05);
  tl.to("#s10-phone", { scale: 1, y: 0, duration: 0.85, ease: "power3.inOut" }, 14.3);
  tl.fromTo("#s10-mini", { y: 0 }, { y: -260, duration: 1.4, ease: "sine.inOut" }, 14.4);

  /* ================= S11 · « Transaction sécurisée » (15 → 18) ================= */
  blurIn("#s11-l1 .ch", 15.0, { stagger: 0.035, dur: 0.4 });
  blurIn("#s11-l2 .ch", 15.25, { stagger: 0.035, dur: 0.4 });
  $$("#s11-tiles .ftile").forEach((t, i) => {
    const [, , , , z, rot] = TILES[i];
    tl.fromTo(t, { opacity: 0, z: -900, rotationY: i % 2 ? 50 : -50, rotation: 0, filter: "blur(10px)" }, { opacity: 1, z, rotationY: i % 2 ? -14 : 14, rotation: rot, filter: "blur(0px)", duration: 0.55, ease: "power3.out" }, 15.25 + i * 0.07);
    tl.to(t, { y: i % 2 ? -26 : 26, duration: 1.3, ease: "sine.inOut" }, 15.8);
  });
  ["#s11-st1", "#s11-st2", "#s11-st3"].forEach((sel, i) => {
    const at = 15.85 + i * 0.4;
    blurIn(sel, at, { scale: 0.8, dur: 0.35 });
    tl.fromTo(sel + " .check", { scale: 0 }, { scale: 1, duration: 0.25, ease: "back.out(3)" }, at + 0.15);
    drawCheck(sel + " .ck", at + 0.22);
  });
  // gros zoom qui traverse le titre et le téléphone
  tl.to("#s10-cam", { scale: 4.2, filter: "blur(20px)", opacity: 0, duration: 0.55, ease: "power3.in", transformOrigin: "50% 48%" }, 17.0);
  $$("#s11-bubbles .wbub").forEach((b, i) => {
    tl.fromTo(b, { scale: 0, opacity: 0 }, { scale: 1.3, opacity: 0.9, duration: 0.3, ease: "power2.out" }, 17.35 + i * 0.03);
    tl.to(b, { scale: 1.8, opacity: 0, duration: 0.3, ease: "power2.in" }, 17.75 + i * 0.02);
  });

  /* ================= S12 · garage 3D + avis (18 → 21) ================= */
  tl.fromTo("#s12-tilt", { rotationX: 58, scale: 0.4 }, { rotationX: 58, scale: 1, duration: 0.7, ease: "power3.out" }, 18.0);
  tl.fromTo("#s12-iso", { rotation: -70 }, { rotation: -42, duration: 0.7, ease: "power3.out" }, 18.0);
  tl.fromTo("#s12-iso-wrap", { opacity: 0, filter: "blur(14px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "power2.out" }, 18.0);
  tl.to("#s12-iso", { rotation: -34, duration: 2.3, ease: "none" }, 18.7);
  tl.fromTo("#s12-card", { y: -700, opacity: 0, rotationX: 30, filter: "blur(14px)" }, { y: 0, opacity: 1, rotationX: 0, filter: "blur(0px)", duration: 0.5, ease: "back.out(1.3)" }, 18.5);
  $$("#s12-stars .star-fill").forEach((s, i) => {
    tl.fromTo(s, { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.22, ease: "back.out(3)" }, 18.95 + i * 0.13);
  });
  tl.fromTo("#s12-quote .word", { opacity: 0, y: 18, filter: "blur(6px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, stagger: 0.075, ease: "power2.out" }, 19.55);
  tl.fromTo("#s12-card .rev-foot", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 20.6);
  tl.to("#s12-cam", { scale: 1.4, opacity: 0, filter: "blur(16px)", duration: 0.35, ease: "power2.in" }, 20.95);

  /* ================= S13 · livraison (21 → 22.5) ================= */
  tl.fromTo("#s13-card", { scale: 0.7, rotationX: 18, opacity: 0, filter: "blur(16px)" }, { scale: 1, rotationX: 0, opacity: 1, filter: "blur(0px)", duration: 0.45, ease: "power3.out" }, 21.0);
  tl.fromTo("#s13-img", { scale: 1.15 }, { scale: 1, duration: 1.5, ease: "power1.out" }, 21.0);
  blurIn("#s13-pill .pill", 21.45, { scale: 0.85, y: 40, dur: 0.35 });
  tl.fromTo("#s13-check", { scale: 0 }, { scale: 1, duration: 0.25, ease: "back.out(3)" }, 21.8);
  drawCheck("#s13-check .ck", 21.88);
  whipOut("#s13-cam", 22.35, { scale: 0.8, blur: 18, dur: 0.25 });

  /* ================= S14 · « Vous repartez tranquille. » (22.5 → 24) ================= */
  tl.fromTo("#s14-text .t-line:first-child", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 22.5);
  blurIn("#s14-w2 .ch", 22.55, { stagger: 0.03, dur: 0.35, blur: 22 });
  const arcLen = 1900;
  tl.fromTo("#s14-path", { strokeDasharray: arcLen, strokeDashoffset: arcLen }, { strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut" }, 22.6);
  blurIn("#s14-w3", 23.0, { scale: 1.4, dur: 0.35 });
  tl.fromTo("#s14-key", { x: 520, rotation: 18, opacity: 0 }, { x: 0, rotation: -6, opacity: 1, duration: 0.35, ease: "power3.out" }, 23.0);
  tl.to("#s14-key", { rotation: 7, duration: 0.17, yoyo: true, repeat: 1, ease: "sine.inOut" }, 23.25);
  tl.to("#s14-key", { scale: 0.4, opacity: 0, filter: "blur(10px)", duration: 0.15, ease: "power2.in" }, 23.5);
  tl.to("#s14-path", { opacity: 0, duration: 0.2 }, 23.5);
  tl.fromTo("#s14-halo", { scale: 0.1, opacity: 0 }, { scale: 1.8, opacity: 1, duration: 0.25, ease: "expo.out" }, 23.55);
  tl.to("#s14-halo", { scale: 2.6, opacity: 0, duration: 0.35, ease: "power2.in" }, 23.8);
  tl.fromTo("#s14-burst .spark", { x: 40, scaleX: 0.2, opacity: 0 }, { x: 520, scaleX: 1, opacity: 1, duration: 0.3, ease: "expo.out" }, 23.55);
  tl.to("#s14-burst .spark", { opacity: 0, duration: 0.2 }, 23.8);
  tl.to("#s14-text", { opacity: 0, filter: "blur(12px)", scale: 1.1, duration: 0.2 }, 23.9);

  /* ================= S15 · signature + numéro + boucle (24 → 28.5) ================= */
  tl.fromTo("#s15-logo", { opacity: 0, scale: 0.7, filter: "blur(20px) brightness(3)" }, { opacity: 1, scale: 1, filter: "blur(0px) brightness(1)", duration: 0.45, ease: "expo.out" }, 24.0);
  tl.to("#s15-logo", { opacity: 0.5, duration: 0.04, yoyo: true, repeat: 3, ease: "none" }, 24.35);
  blurIn("#s15-handle", 24.2, { scale: 0.9, dur: 0.3 });
  blurIn("#s15-services .word:not(.red)", 24.5, { stagger: 0.14, scale: 1.2, dur: 0.3 });
  blurIn("#s15-services .word.red", 25.0, { scale: 1.5, dur: 0.35 });
  blurIn("#s15-city", 25.2, { scale: 1, y: 20, dur: 0.3 });
  // bouton d'appel : il surgit, les chiffres arrivent deux par deux, le combiné sonne, l'anneau pulse
  tl.fromTo("#s15-call", { opacity: 0, scale: 0.6, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "back.out(1.8)" }, 25.45);
  blurIn("#s15-num .pair", 25.55, { stagger: 0.07, scale: 1.4, dur: 0.3 });
  [25.95, 26.85].forEach((t0) => {
    [-16, 16, -14, 14, -9, 9, 0].forEach((r, i) => tl.to("#s15-ico svg", { rotation: r, duration: 0.05, ease: "sine.inOut" }, t0 + i * 0.05));
  });
  tl.fromTo(
    "#s15-call",
    { boxShadow: "0 0 0 0px rgba(255, 79, 112, 0.6), 0 18px 50px rgba(255, 79, 112, 0.45)" },
    { boxShadow: "0 0 0 34px rgba(255, 79, 112, 0), 0 18px 70px rgba(255, 79, 112, 0.7)", duration: 0.6, repeat: 2, ease: "power2.out", immediateRender: false },
    25.9,
  );
  // tout se contracte vers le point rouge du début → boucle
  tl.to("#s15-cam", { scale: 0.02, opacity: 0, filter: "blur(8px)", duration: 0.55, ease: "power3.in", transformOrigin: "50% 50%" }, 27.55);
  tl.fromTo("#s15-dot", { rotation: 45 + 180, scale: 6, opacity: 0 }, { rotation: 45, scale: 1, opacity: 1, duration: 0.6, ease: "power3.out" }, 27.85);
  tl.fromTo("#s15-halo", { scale: 1.4, opacity: 0 }, { scale: 0.35, opacity: 0.7, duration: 0.6, ease: "power3.out" }, 27.85);

  return tl;
};
