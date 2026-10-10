// Flat vector art for the Bikini Shop film. Every function returns an SVG string;
// scenes inject them at setup (before their timeline is built). No randomness.
(function () {
  const C = {
    orange: "#F26B21",
    orangeDeep: "#C9471A",
    cream: "#FFF3E4",
    ink: "#24121C",
    pink: "#FF2E7E",
    pinkDeep: "#C4165E",
    gold: "#F4B533",
    goldDeep: "#B9761C",
    teal: "#12A89A",
    blue: "#2F6FD6",
  };

  // ---------------------------------------------------------------- hibiscus
  function hibiscus(o) {
    o = o || {};
    const petal = o.petal || C.pink;
    const vein = o.vein || "rgba(255,255,255,0.35)";
    const heart = o.heart || C.pinkDeep;
    const id = o.id || "h";
    let petals = "";
    for (let i = 0; i < 5; i++) {
      const r = i * 72 - 90;
      petals +=
        '<g class="' + id + '-petal" transform="rotate(' + r + ' 200 200)">' +
        '<path d="M200 200 C 150 150, 150 40, 205 30 C 265 25, 275 140, 200 200 Z" fill="' + petal + '"/>' +
        '<path d="M200 196 C 196 150, 200 90, 208 52" stroke="' + vein + '" stroke-width="5" fill="none" stroke-linecap="round"/>' +
        "</g>";
    }
    return (
      '<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">' +
      petals +
      '<circle cx="200" cy="200" r="38" fill="' + heart + '"/>' +
      '<g class="' + id + '-stamen"><path d="M200 200 C 215 170, 240 140, 262 112" stroke="' + C.gold + '" stroke-width="9" fill="none" stroke-linecap="round"/>' +
      '<circle cx="262" cy="112" r="11" fill="' + C.gold + '"/><circle cx="248" cy="104" r="8" fill="' + C.gold + '"/><circle cx="272" cy="126" r="8" fill="' + C.gold + '"/></g>' +
      "</svg>"
    );
  }

  // ---------------------------------------------------------------- patterns for swimwear
  function patterns(pfx) {
    return (
      "<defs>" +
      // pink crochet: dots on hot pink
      '<pattern id="' + pfx + '-crochet" width="22" height="22" patternUnits="userSpaceOnUse">' +
      '<rect width="22" height="22" fill="#E8326E"/><circle cx="11" cy="11" r="6" fill="none" stroke="#FF8FB4" stroke-width="3"/></pattern>' +
      // blue hibiscus print
      '<pattern id="' + pfx + '-flora" width="70" height="70" patternUnits="userSpaceOnUse">' +
      '<rect width="70" height="70" fill="' + C.blue + '"/>' +
      '<g fill="#DCEBFF"><ellipse cx="20" cy="12" rx="7" ry="12"/><ellipse cx="30" cy="24" rx="12" ry="7"/><ellipse cx="10" cy="24" rx="12" ry="7"/><ellipse cx="14" cy="36" rx="7" ry="11" transform="rotate(30 14 36)"/><ellipse cx="27" cy="36" rx="7" ry="11" transform="rotate(-30 27 36)"/></g>' +
      '<circle cx="20" cy="26" r="5" fill="' + C.gold + '"/><circle cx="56" cy="58" r="6" fill="#9CC2FF"/><circle cx="52" cy="10" r="3" fill="#9CC2FF"/></pattern>' +
      // leopard
      '<pattern id="' + pfx + '-leo" width="60" height="60" patternUnits="userSpaceOnUse">' +
      '<rect width="60" height="60" fill="#C99A5B"/>' +
      '<g fill="none" stroke="#3B2414" stroke-width="5" stroke-linecap="round"><path d="M8 10 q8 -6 14 2"/><path d="M38 6 q9 2 8 11"/><path d="M14 40 q-4 8 4 13"/><path d="M44 36 q10 -1 10 9"/></g>' +
      '<g fill="#6B4320"><circle cx="15" cy="14" r="4"/><circle cx="42" cy="12" r="4"/><circle cx="19" cy="46" r="4"/><circle cx="49" cy="42" r="4"/></g></pattern>' +
      // teal waves
      '<pattern id="' + pfx + '-wave" width="48" height="24" patternUnits="userSpaceOnUse">' +
      '<rect width="48" height="24" fill="' + C.teal + '"/><path d="M0 12 q12 -10 24 0 t24 0" fill="none" stroke="#9FF0E4" stroke-width="3.5"/></pattern>' +
      // gold shine for the mannequin
      '<linearGradient id="' + pfx + '-gold" x1="0" y1="0" x2="1" y2="0">' +
      '<stop offset="0" stop-color="#A8661A"/><stop offset="0.28" stop-color="#E9A93A"/><stop offset="0.5" stop-color="#FFD978"/><stop offset="0.72" stop-color="#E9A93A"/><stop offset="1" stop-color="#9A5A14"/></linearGradient>' +
      '<linearGradient id="' + pfx + '-black" x1="0" y1="0" x2="1" y2="0">' +
      '<stop offset="0" stop-color="#0E0A0D"/><stop offset="0.35" stop-color="#2E2530"/><stop offset="0.48" stop-color="#6E6470"/><stop offset="0.6" stop-color="#2E2530"/><stop offset="1" stop-color="#0E0A0D"/></linearGradient>' +
      "</defs>"
    );
  }

  const TORSO =
    "M172 18 h56 v44 C 238 74, 298 74, 330 96 C 348 108, 344 142, 326 172 C 310 230, 300 282, 286 322 " +
    "C 279 344, 288 384, 312 432 C 334 482, 322 544, 296 596 L 214 596 C 210 566, 205 548, 200 542 " +
    "C 195 548, 190 566, 186 596 L 104 596 C 78 544, 66 482, 88 432 C 112 384, 121 344, 114 322 " +
    "C 100 282, 90 230, 74 172 C 56 142, 52 108, 70 96 C 102 74, 162 74, 172 62 Z";

  // swimwear looks — fills reference pattern ids built by patterns(pfx)
  const LOOKS = {
    crochet: { top: "crochet", bottom: "crochet", pareo: null, flower: true },
    flora: { top: "flora", bottom: "flora", pareo: "flora", flower: false },
    leo: { top: "solid:#4A2A1A", bottom: "leo", pareo: "leo", flower: false },
    red: { top: "solid:#E0262E", bottom: "solid:#E0262E", pareo: null, flower: false },
    wave: { top: "wave", bottom: "wave", pareo: null, flower: true },
    one: { one: "solid:#EADBC6", flower: false },
  };

  function fill(pfx, f) {
    return f.indexOf("solid:") === 0 ? f.slice(6) : "url(#" + pfx + "-" + f + ")";
  }

  function swimwear(pfx, look) {
    const L = LOOKS[look];
    const S = 'stroke="rgba(36,18,28,0.35)" stroke-width="3"';
    if (L.one) {
      const f = fill(pfx, L.one);
      return (
        '<path d="M178 62 L150 170 C 135 230, 140 290, 128 330 C 120 380, 126 420, 140 462 L200 520 L260 462 C 274 420, 280 380, 272 330 C 260 290, 265 230, 250 170 L222 62 L212 62 L200 190 L188 62 Z" fill="' + f + '" ' + S + "/>" +
        '<path d="M150 300 C 190 286, 210 286, 250 300" stroke="#C9B49A" stroke-width="5" fill="none"/>'
      );
    }
    const top = fill(pfx, L.top);
    const bot = fill(pfx, L.bottom);
    let out =
      // neck strings
      '<path d="M152 168 L184 64 M248 168 L216 64" stroke="' + C.ink + '" stroke-width="5" stroke-linecap="round"/>' +
      // band
      '<path d="M84 262 C 140 272, 260 272, 316 262" stroke="' + C.ink + '" stroke-width="5" fill="none"/>' +
      // cups
      '<path d="M152 164 C 128 200, 108 236, 104 262 C 140 272, 180 272, 198 266 C 194 226, 176 190, 152 164 Z" fill="' + top + '" ' + S + "/>" +
      '<path d="M248 164 C 272 200, 292 236, 296 262 C 260 272, 220 272, 202 266 C 206 226, 224 190, 248 164 Z" fill="' + top + '" ' + S + "/>" +
      // bottom
      '<path d="M96 448 C 150 466, 250 466, 304 448 L 300 462 C 270 480, 240 506, 222 548 C 210 560, 190 560, 178 548 C 160 506, 130 480, 100 462 Z" fill="' + bot + '" ' + S + "/>" +
      '<path d="M92 446 C 150 462, 250 462, 308 446" stroke="' + C.ink + '" stroke-width="5" fill="none"/>';
    if (L.pareo) {
      out +=
        '<path d="M86 436 C 150 452, 250 452, 314 436 C 328 480, 330 540, 320 596 L 210 596 C 200 560, 160 520, 150 470 C 130 510, 110 560, 100 596 L 80 596 C 74 540, 76 480, 86 436 Z" fill="' + fill(pfx, L.pareo) + '" opacity="0.92" ' + S + "/>" +
        '<path d="M150 450 C 140 470, 150 486, 168 478 C 186 470, 176 446, 150 450 Z" fill="' + C.ink + '" opacity="0.35"/>';
    }
    if (L.flower) {
      out += '<g transform="translate(168 236) scale(0.16)">' + hibiscus({ petal: "#FFF6EC", heart: C.gold, vein: "rgba(242,107,33,0.35)" }) .replace("<svg", "<svg width=\"400\" height=\"400\"") + "</g>";
    }
    return out;
  }

  // Mannequin with every look stacked as <g class="look look-NAME">; scenes cross-fade them.
  function mannequin(pfx, looks, black) {
    let s =
      '<svg viewBox="0 0 400 600" xmlns="http://www.w3.org/2000/svg">' +
      patterns(pfx) +
      '<path d="' + TORSO + '" fill="url(#' + pfx + (black ? "-black" : "-gold") + ')"/>' +
      '<ellipse cx="160" cy="210" rx="16" ry="60" fill="#FFFFFF" opacity="' + (black ? 0.18 : 0.28) + '"/>' +
      '<ellipse cx="248" cy="410" rx="12" ry="54" fill="#FFFFFF" opacity="' + (black ? 0.14 : 0.22) + '"/>' +
      '<rect x="172" y="0" width="56" height="24" rx="6" fill="' + (black ? "#1A1418" : C.goldDeep) + '"/>';
    looks.forEach((lk) => {
      s += '<g class="look look-' + lk + '">' + swimwear(pfx, lk) + "</g>";
    });
    return s + "</svg>";
  }

  // ---------------------------------------------------------------- icons (stroke ink, 120 box)
  const ICON = {
    sun:
      '<circle cx="60" cy="60" r="22" fill="' + C.gold + '"/>' +
      [0, 45, 90, 135, 180, 225, 270, 315]
        .map((a) => '<rect x="56" y="12" width="8" height="18" rx="4" fill="' + C.gold + '" transform="rotate(' + a + ' 60 60)"/>')
        .join(""),
    beach:
      '<circle cx="84" cy="34" r="16" fill="' + C.gold + '"/>' +
      '<path d="M10 78 q12 -10 25 0 t25 0 t25 0 t25 0" fill="none" stroke="' + C.teal + '" stroke-width="7" stroke-linecap="round"/>' +
      '<path d="M10 98 q12 -10 25 0 t25 0 t25 0 t25 0" fill="none" stroke="' + C.teal + '" stroke-width="7" stroke-linecap="round" opacity="0.6"/>' +
      '<path d="M40 74 L40 22" stroke="' + C.ink + '" stroke-width="5"/><path d="M14 30 C 20 6, 62 6, 68 30 Z" fill="' + C.pink + '"/>',
    pool:
      '<rect x="12" y="62" width="96" height="44" rx="10" fill="#7FD8F0"/>' +
      '<path d="M18 80 q10 -8 20 0 t20 0 t20 0 t20 0" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>' +
      '<path d="M40 70 V22 a12 12 0 0 1 24 0 M80 70 V22 a12 12 0 0 1 24 0" fill="none" stroke="' + C.ink + '" stroke-width="7" stroke-linecap="round"/>' +
      '<path d="M40 38 H80 M40 56 H80" stroke="' + C.ink + '" stroke-width="6"/>',
    plane:
      '<path d="M10 66 L52 58 L84 18 C 90 10, 104 12, 100 24 L84 62 L112 76 L104 84 L76 78 L58 104 L48 102 L54 74 L14 76 Z" fill="' + C.pink + '" stroke="' + C.ink + '" stroke-width="4" stroke-linejoin="round"/>',
    heart:
      '<path d="M60 104 C 20 76, 6 54, 14 34 C 22 14, 50 12, 60 34 C 70 12, 98 14, 106 34 C 114 54, 100 76, 60 104 Z" fill="' + C.pink + '"/>',
    chat:
      '<path d="M16 22 h88 a10 10 0 0 1 10 10 v46 a10 10 0 0 1 -10 10 h-50 l-24 20 v-20 h-14 a10 10 0 0 1 -10 -10 v-46 a10 10 0 0 1 10 -10 Z" fill="' + C.teal + '"/>' +
      '<circle cx="38" cy="56" r="7" fill="#FFF"/><circle cx="60" cy="56" r="7" fill="#FFF"/><circle cx="82" cy="56" r="7" fill="#FFF"/>',
    pin:
      '<path d="M60 112 C 30 74, 20 58, 20 42 a40 40 0 0 1 80 0 c0 16 -10 32 -40 70 Z" fill="' + C.pink + '"/><circle cx="60" cy="42" r="15" fill="#FFF3E4"/>',
    house:
      '<path d="M14 58 L60 18 L106 58" fill="none" stroke="' + C.ink + '" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>' +
      '<path d="M26 54 V104 H94 V54" fill="#FFF3E4" stroke="' + C.ink + '" stroke-width="7" stroke-linejoin="round"/>' +
      '<rect x="50" y="70" width="20" height="34" fill="' + C.orange + '"/>',
    box:
      '<rect x="16" y="40" width="88" height="66" rx="6" fill="#E3A86A" stroke="' + C.ink + '" stroke-width="5"/>' +
      '<path d="M16 58 H104 M60 40 V106" stroke="' + C.ink + '" stroke-width="5"/>' +
      '<path d="M60 40 C 40 18, 24 30, 40 40 M60 40 C 80 18, 96 30, 80 40" fill="none" stroke="' + C.pink + '" stroke-width="7" stroke-linecap="round"/>',
    phone:
      '<rect x="34" y="8" width="52" height="104" rx="12" fill="' + C.ink + '"/><rect x="40" y="20" width="40" height="76" rx="4" fill="' + C.pink + '"/>',
    call:
      '<path d="M30 18 C 22 18, 14 26, 16 36 C 22 70, 50 98, 84 104 C 94 106, 102 98, 102 90 L 102 78 C 102 74, 99 71, 95 70 L 78 66 C 74 65, 70 67, 68 70 L 64 77 C 52 71, 49 68, 43 56 L 50 52 C 53 50, 55 46, 54 42 L 50 25 C 49 21, 46 18, 42 18 Z" fill="' + C.cream + '"/>',
    sparkle:
      '<path d="M60 6 C 64 44, 76 56, 114 60 C 76 64, 64 76, 60 114 C 56 76, 44 64, 6 60 C 44 56, 56 44, 60 6 Z" fill="' + C.gold + '"/>',
    shades:
      '<path d="M6 40 H114" stroke="' + C.ink + '" stroke-width="8" stroke-linecap="round"/>' +
      '<path d="M12 40 h40 c0 26 -8 36 -22 36 c-14 0 -18 -14 -18 -36 Z M68 40 h40 c0 22 -4 36 -18 36 c-14 0 -22 -10 -22 -36 Z" fill="' + C.ink + '"/>' +
      '<path d="M20 48 l10 -2 M76 48 l10 -2" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.6"/>',
    leaf:
      '<path d="M60 8 L70 40 L104 34 L84 60 L110 84 L74 82 L60 114 L46 82 L10 84 L36 60 L16 34 L50 40 Z" fill="' + C.orangeDeep + '"/>',
  };

  function icon(name, extra) {
    return '<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg"' + (extra || "") + ">" + ICON[name] + "</svg>";
  }

  // tiny seeded PRNG for decorative layouts
  function rng(seed) {
    let s = seed >>> 0;
    return function () {
      s = (s + 0x6d2b79f5) >>> 0;
      let t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  window.ART = { C, hibiscus, mannequin, icon, rng, LOOKS: Object.keys(LOOKS) };
})();
