/* Y-K Design — timeline maîtresse unique (GSAP, en pause, pilotée par le temps de composition).
   Tous les repères sont en images (f) à 30 i/s : F(f) = f / 30. Les coupes franches sont portées par les
   fenêtres des <section> dans index.html ; ici, seulement les mouvements à l'intérieur des plans. */
window.buildYK = function () {
  const tl = gsap.timeline({ paused: true });
  const F = (f) => f / 30;
  const $ = (s) => document.querySelector(s);
  const IMG = { baskets: "assets/images/baskets.webp", parfum: "assets/images/parfum.webp", sac: "assets/images/sac.webp" };

  // ---- registre des cartes (assets/CARTES.json) : affiches, gros plans par recadrage, cartes typographiques
  const CARDS = {
    sneaker_poster: { img: IMG.baskets, scale: 1, focus: [0.5, 0.5] },
    perfume_poster: { img: IMG.parfum, scale: 1, focus: [0.5, 0.5] },
    handbag_poster: { img: IMG.sac, scale: 1, focus: [0.5, 0.5] },
    sneaker_detail: { img: IMG.baskets, scale: 2.8, focus: [0.76, 0.48] },
    perfume_detail: { img: IMG.parfum, scale: 3.5, focus: [0.61, 0.54] },
    handbag_detail: { img: IMG.sac, scale: 2.8, focus: [0.5, 0.65] },
    style_type: { text: "STYLE", cls: "type-style" },
    signature_type: { text: "SIGNATURE", cls: "type-signature" },
    allure_type: { text: "ALLURE", cls: "type-allure" },
  };
  function cardContent(el, id) {
    const c = CARDS[id];
    if (c.text) {
      el.classList.add("type", c.cls);
      el.innerHTML = `<span>${c.text}</span>`;
    } else {
      const im = document.createElement("img");
      im.src = c.img;
      im.alt = "";
      if (c.scale !== 1) {
        im.style.transformOrigin = `${c.focus[0] * 100}% ${c.focus[1] * 100}%`;
        im.style.transform = `scale(${c.scale})`;
      }
      el.appendChild(im);
    }
    el.dataset.card = id;
    return el;
  }

  /* =============== A · S01–S04 (f0–151) =============== */
  // bloc marque : origine du groupe au centre du cadre ; monogramme 90 px de large (silhouette visible)
  const MW = 90, MH = (90 * 721) / 1641;
  const NAME_W = 5.4942 * 64; // « Y-K Design », Inter 700, 64 px
  const LOCK_W = MW + 18 + NAME_W;
  const MONO_X = -LOCK_W / 2 + MW / 2; // centre final du monogramme
  const NAME_X = -LOCK_W / 2 + MW + 18;
  gsap.set("#a-lock", { x: 960, y: 540 });
  gsap.set("#a-mono", { x: -MW / 2, y: -MH / 2, transformOrigin: "50% 50%" });
  gsap.set("#a-name-mask", { x: NAME_X, y: -36, width: 0, height: 72 });
  gsap.set("#a-name", { y: 4 });
  gsap.set("#a-caption", { x: -131, y: 52, autoAlpha: 0 });

  // S01 : recul très rapide depuis une taille géante, léger passage sous la taille finale, stabilisation
  tl.fromTo("#a-mono", { scale: 60 }, { scale: 153.75 / 90, duration: F(6), ease: "power2.out" }, 0);
  tl.to("#a-mono", { scale: 71.25 / 90, duration: F(6), ease: "power1.out" }, F(6));
  tl.to("#a-mono", { scale: 1, duration: F(18), ease: "power2.inOut" }, F(12));
  // S02 : le monogramme glisse à gauche (même taille), le nom se révèle à droite, puis le bloc monte
  tl.to("#a-mono", { x: MONO_X - MW / 2, duration: F(22), ease: "power2.inOut" }, F(44));
  tl.to("#a-name-mask", { width: NAME_W + 8, duration: F(18), ease: "power2.out" }, F(48));
  tl.to("#a-caption", { autoAlpha: 1, duration: F(8), ease: "none" }, F(80));
  tl.to("#a-lock", { y: 92, duration: F(30), ease: "power2.inOut" }, F(70));
  tl.to("#a-lock", { y: -160, duration: F(18), ease: "power1.in" }, F(110));

  // S03–S04 : galerie quatre colonnes, chaque colonne est un groupe masqué autonome qui défile vers le haut
  const COLS = [
    { off: 0, cards: [["sneaker_poster", 375], ["style_type", 250], ["handbag_detail", 440], ["perfume_poster", 375]] },
    { off: 110, cards: [["perfume_detail", 470], ["handbag_poster", 375], ["signature_type", 250], ["sneaker_detail", 400]] },
    { off: -40, cards: [["handbag_poster", 375], ["sneaker_detail", 330], ["perfume_poster", 375], ["allure_type", 250]] },
    { off: 60, cards: [["sneaker_detail", 430], ["perfume_poster", 375], ["allure_type", 250], ["handbag_poster", 375]] },
  ];
  const gal = $("#a-gallery");
  COLS.forEach((col, c) => {
    const box = document.createElement("div");
    box.className = "col";
    box.style.left = `${165 + c * 405}px`;
    const inner = document.createElement("div");
    inner.className = "col-in";
    let y = 0;
    col.cards.forEach(([id, h], k) => {
      const card = cardContent(document.createElement("div"), id);
      card.className += " card";
      card.style.top = `${y}px`;
      card.style.height = `${h}px`;
      inner.appendChild(card);
      y += h + 30;
      // entrées décalées : les premières cartes de droite à gauche, les suivantes quand la colonne les amène
      const at = k < 2 ? 84 + (3 - c) * 5 + k * 8 : k === 2 ? 110 + c * 4 : 126 + c * 4;
      gsap.set(card, { autoAlpha: 0 });
      tl.fromTo(card, { y: k < 2 ? 90 : 40, autoAlpha: 0.25 }, { y: 0, autoAlpha: 1, duration: F(k < 2 ? 12 : 10), ease: "power2.out", immediateRender: false }, F(at));
    });
    inner.style.height = `${y - 30}px`;
    box.appendChild(inner);
    gal.appendChild(box);
    const start = 440 + col.off;
    const end = 1120 - (y - 30);
    // défilement continu de f80 jusqu'à la coupe (f152) : pas d'arrêt au passage f117
    tl.fromTo(inner, { y: start }, { y: end, duration: F(152 - 80), ease: "power1.in" }, F(80));
  });

  /* =============== B · S05–S09 (f152–367) =============== */
  // S05 : « Des publicités » + cartouche clair ; le groupe se recentre selon la largeur du mot (Inter 700, 66 px,
  // largeurs mesurées dans la page : préfixe 456,2 px, écart 20 px, cartouche = mot + 40 px)
  const PRE_L = [552.35, 502.65, 520.55, 456.95];
  const CART_W = [339.1, 438.5, 402.7, 529.9];
  const CART_DX = 476.2;
  gsap.set("#b-sentence", { transformOrigin: "960px 540px" });
  gsap.set("#b-prefix", { x: PRE_L[0], y: 494 });
  gsap.set("#b-cart", { x: PRE_L[0] + CART_DX, y: 494, width: CART_W[0] });
  gsap.set("#b-strip", { y: 0 });
  gsap.set("#b-vos-mask", { x: 917.55, y: 494, width: 0 });
  tl.fromTo("#b-sentence", { scale: 1.16 }, { scale: 1, duration: F(14), ease: "power2.out" }, F(152));
  // chaque mot n'existe que pendant sa présence dans le cartouche (entrée, maintien, sortie)
  const WORDS = gsap.utils.toArray("#b-strip div");
  const WIN = [[152, 185], [179, 201], [195, 217], [211, 240], [234, 276]];
  gsap.set(WORDS, { autoAlpha: 0 });
  WIN.forEach(([a, b], i) => {
    tl.set(WORDS[i], { autoAlpha: 1 }, F(a));
    tl.set(WORDS[i], { autoAlpha: 0 }, F(b));
  });
  [179, 195, 211].forEach((f, i) => {
    const n = i + 1;
    tl.to("#b-strip", { y: -92 * n, duration: F(6), ease: "power2.inOut" }, F(f));
    tl.to("#b-prefix", { x: PRE_L[n], duration: F(6), ease: "power2.inOut" }, F(f));
    tl.to("#b-cart", { x: PRE_L[n] + CART_DX, width: CART_W[n], duration: F(6), ease: "power2.inOut" }, F(f));
  });
  // S06 : « Je réalise » remplace le mot, le préfixe sort, « vos montages » se révèle, punch-in f257
  const JE_W = 4.6836 * 66 + 40;
  tl.to("#b-strip", { y: -368, duration: F(6), ease: "power2.inOut" }, F(234));
  tl.to("#b-prefix", { autoAlpha: 0, x: PRE_L[3] - 140, duration: F(5), ease: "power2.in" }, F(234));
  tl.to("#b-cart", { x: 548.45, width: JE_W, duration: F(10), ease: "power2.inOut" }, F(236));
  tl.to("#b-vos-mask", { width: 460, duration: F(9), ease: "power2.out" }, F(246));
  tl.to("#b-sentence", { scale: 2.2, duration: F(4), ease: "power3.out" }, F(255));
  tl.to("#b-cart", { x: -360, duration: F(14), ease: "power2.in" }, F(262));
  tl.to("#b-vos-mask", { x: 733, duration: F(14), ease: "power2.inOut" }, F(262));

  // S07 : six cartes en couronne ; les centres tournent dans le sens horaire, les images restent droites
  const ORDER = ["sneaker_poster", "perfume_poster", "sneaker_detail", "handbag_detail", "perfume_detail", "handbag_poster"];
  const RX = 430, RY = 330, SIDE = 250;
  const ringEls = ORDER.map((id) => {
    const el = cardContent(document.createElement("div"), id);
    el.className += " abs ring";
    $("#b-ring").appendChild(el);
    return el;
  });
  const hero = ringEls[1];
  hero.insertAdjacentHTML("beforeend", '<div id="b-veil"></div><div id="b-btn">Créer ma publicité</div>');
  const ring = { rho: 0.25, th: -150 };
  const placeRing = () => {
    ringEls.forEach((el, i) => {
      const a = ((ring.th + i * 60) * Math.PI) / 180;
      gsap.set(el, { x: 960 + RX * ring.rho * Math.cos(a) - SIDE / 2, y: 540 + RY * ring.rho * Math.sin(a) - SIDE / 2 });
    });
  };
  placeRing();
  gsap.set(ringEls, { autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%" });
  tl.to("#b-sentence", { scale: 1.15, duration: F(8), ease: "power3.out" }, F(284));
  tl.to(ringEls, { autoAlpha: 1, scale: 1, duration: F(8), ease: "power2.out", stagger: F(0.5) }, F(284));
  tl.to(ring, { rho: 1, duration: F(10), ease: "back.out(1.4)", onUpdate: placeRing }, F(284));
  tl.to(ring, { th: -60, duration: F(52), ease: "power1.out", onUpdate: placeRing }, F(284));

  // S08 : un curseur blanc survole le parfum (à droite), voile discret, bouton Créer ma publicité, appui f343
  const TIP = [3.45, 2.3];
  const cur = (x, y) => ({ x: x - TIP[0], y: y - TIP[1] });
  gsap.set("#b-cursor", { ...cur(1720, 990), autoAlpha: 0, transformOrigin: "8% 5%" });
  tl.to("#b-cursor", { autoAlpha: 1, duration: F(2), ease: "none" }, F(326));
  tl.to("#b-cursor", { ...cur(1400, 575), duration: F(5), ease: "power2.out" }, F(326));
  tl.to("#b-veil", { opacity: 1, duration: F(3), ease: "none" }, F(331));
  tl.fromTo("#b-btn", { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: F(4), ease: "back.out(2)" }, F(333));
  tl.to("#b-cursor", { ...cur(1428, 452), duration: F(5), ease: "power2.inOut" }, F(331));
  tl.to("#b-btn", { scale: 0.9, backgroundColor: "#9e0c21", duration: F(3), ease: "power2.out" }, F(340));
  tl.to("#b-cursor", { scale: 0.88, duration: F(3), ease: "power2.out" }, F(340));
  tl.to("#b-btn", { scale: 1, backgroundColor: "#bd0f28", duration: F(4), ease: "power2.out" }, F(345));
  tl.to("#b-cursor", { scale: 1, duration: F(4), ease: "power2.out" }, F(345));

  // S09 : punch-in du groupe (≈2,4) puis translation pour amener le même parfum près du centre
  gsap.set("#b-zoom", { transformOrigin: "1294px 540px" });
  tl.to("#b-zoom", { scale: 2.4, duration: F(3), ease: "power3.out" }, F(344));
  tl.to("#b-zoom", { x: -545, y: -43, duration: F(12), ease: "power3.out" }, F(346));
  tl.to("#b-zoom", { x: -560, duration: F(9), ease: "power1.out" }, F(358));

  /* =============== C · S10–S12 (f368–523) =============== */
  gsap.set("#c-modal", { transformOrigin: "615px 387px" });
  tl.fromTo("#c-modal", { autoAlpha: 0.3, scale: 0.94 }, { autoAlpha: 1, scale: 1, duration: F(6), ease: "power2.out" }, F(368));
  // S10 : frappe pré-calculée (dossier/scenes/SCENE_10.json) et curseur texte qui clignote
  const TYPING = [[380, "V"], [382, "Vo"], [385, "Vot"], [388, "Votr"], [391, "Votre"], [394, "Votre "], [397, "Votre b"], [400, "Votre bo"], [403, "Votre bou"], [406, "Votre bout"], [409, "Votre bouti"], [412, "Votre boutiq"], [414, "Votre boutiqu"], [416, "Votre boutique"]];
  tl.set("#c-typed", { textContent: "" }, 0);
  TYPING.forEach(([f, v]) => tl.set("#c-typed", { textContent: v }, F(f)));
  for (let f = 368; f < 459; f += 8) {
    const typing = f >= 376 && f < 420;
    tl.set("#c-caret", { opacity: typing ? 1 : (f / 8) % 2 < 1 ? 1 : 0 }, F(f));
  }
  gsap.set("#c-cursor", { ...cur(1260, 650), autoAlpha: 0, transformOrigin: "8% 5%" });
  tl.to("#c-cursor", { autoAlpha: 1, duration: F(4), ease: "none" }, F(416));
  tl.to("#c-cursor", { ...cur(1004, 824), duration: F(16), ease: "power2.inOut" }, F(418));
  // S11 : appui, puis spinner blanc fini dans le même bouton (rotation pilotée par la timeline)
  tl.to("#c-btn", { scale: 0.97, backgroundColor: "#9e0c21", duration: F(3), ease: "power2.out" }, F(438));
  tl.to("#c-cursor", { scale: 0.88, duration: F(3), ease: "power2.out" }, F(438));
  tl.to("#c-btn", { scale: 1, backgroundColor: "#bd0f28", duration: F(4), ease: "power2.out" }, F(442));
  tl.to("#c-cursor", { scale: 1, duration: F(4), ease: "power2.out" }, F(442));
  tl.to("#c-btn-label", { autoAlpha: 0, duration: F(2), ease: "none" }, F(443));
  tl.set("#c-spin", { autoAlpha: 1, rotation: 0 }, F(444));
  tl.to("#c-spin", { rotation: 720, duration: F(14), ease: "none" }, F(444));
  // S12 : le modal se ferme, carte sombre « Montages pour boutiques » + numéro, zoom vers 16,10 s puis pause
  tl.to("#c-modal", { autoAlpha: 0, scale: 0.94, duration: F(6), ease: "power2.in" }, F(459));
  tl.to("#c-cursor", { autoAlpha: 0, duration: F(4), ease: "none" }, F(459));
  tl.fromTo("#c-card", { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: F(9), ease: "power3.out" }, F(461));
  tl.to("#c-zoom", { scale: 1.45, duration: F(14), ease: "power2.inOut" }, F(476));

  /* =============== D–H · S13–S17 (f524–622) =============== */
  tl.fromTo("#d-q", { autoAlpha: 0.4, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: F(5), ease: "back.out(2)" }, F(524));
  tl.fromTo("#d-w", { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: F(5), ease: "back.out(2)" }, F(530));
  tl.fromTo("#d-num", { autoAlpha: 0, y: 12 }, { autoAlpha: 1, y: 0, duration: F(6), ease: "power2.out" }, F(534));
  tl.fromTo("#e-avec", { scale: 1.12 }, { scale: 1, duration: F(5), ease: "power3.out" }, F(555));
  tl.fromTo("#f-mono", { scale: 1.08 }, { scale: 1, duration: F(5), ease: "power3.out" }, F(573));
  tl.fromTo("#g-name", { scale: 1.08 }, { scale: 1, duration: F(5), ease: "power3.out" }, F(584));
  tl.fromTo("#h-lock", { autoAlpha: 0.4, y: 20 }, { autoAlpha: 1, y: 0, duration: F(7), ease: "power2.out" }, F(596));
  tl.fromTo("#h-sub", { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: F(7), ease: "power2.out" }, F(600));
  tl.fromTo("#h-num", { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: F(7), ease: "power2.out" }, F(604));
  // la signature tient jusqu'à f622, sans fondu ; la timeline couvre toute la durée
  tl.set({}, {}, F(623));
  return tl;
};
