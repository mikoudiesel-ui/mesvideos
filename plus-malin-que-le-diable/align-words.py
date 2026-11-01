"""Word timings for this project: the phrase runs come from onsets.py (real sound), the words of each phrase are
spread over its run in proportion to their vowel groups. Writes onsets.json and assets/audio/voix-montage-mots.json."""
import json, re, pathlib
here = pathlib.Path(__file__).parent
P = [(0.49, 0.97, "Lundi,"), (1.51, 2.61, "tu te promets de commencer."), (3.93, 4.56, "Mercredi,"),
     (5.25, 5.81, "tu repousses."), (6.93, 7.75, "Dimanche soir..."), (8.68, 9.36, "rien n'a bougé."),
     (12.78, 14.11, "Ce n'est pas un manque de talent."), (14.95, 15.78, "C'est une petite voix."),
     (16.88, 17.81, "Elle te dit d'attendre,"), (18.55, 19.27, "que ce n'est pas pour toi,"),
     (19.92, 20.57, "que demain,"), (20.92, 21.37, "ce sera mieux."),
     (22.74, 24.57, "Et si tu étais plus malin qu'elle ?"), (26.24, 27.45, "Plus malin que le diable."),
     (28.10, 28.86, "Un ebook qui démasque"), (29.00, 29.97, "ses ruses,"), (30.15, 30.73, "une par une."),
     (31.56, 32.88, "Et te donne de quoi lui répondre."), (33.24, 34.42, "Télécharge-le maintenant,"),
     (34.76, 35.64, "le lien est juste en dessous.")]
def weight(w):
    return max(1, len(re.findall(r"[aeiouyéèêàâîôûœ]+", w.lower()))) + 0.3
words, phrases = [], []
for s, e, text in P:
    toks = [t for t in text.replace(" ?", "?").split() if t]
    tot = sum(weight(t) for t in toks); t0 = s; idx = []
    for t in toks:
        d = (e - s) * weight(t) / tot
        idx.append(len(words)); words.append({"w": t, "s": round(t0, 2), "e": round(t0 + d, 2)}); t0 += d
    phrases.append({"start": s, "end": e, "text": text, "words": idx})
json.dump({"audio": "assets/audio/voix-montage.wav", "duration": 38.5, "phrases": phrases, "words": words},
          open(here / "onsets.json", "w"), ensure_ascii=False, indent=1)
json.dump({"duration": 38.5, "words": [{"w": x["w"], "start": x["s"], "end": x["e"]} for x in words]},
          open(here / "assets/audio/voix-montage-mots.json", "w"), ensure_ascii=False, indent=1)
print(len(words), "words")
