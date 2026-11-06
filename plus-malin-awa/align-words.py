"""Word timings for this project: the phrase runs come from onsets.py (real sound), the words of each phrase are
spread over its run in proportion to their vowel groups. Writes onsets.json and assets/audio/voix-montage-mots.json."""
import json, re, pathlib
here = pathlib.Path(__file__).parent
P = [(0.32, 1.10, "Chaque « demain »"), (1.28, 2.21, "te coûte un rêve."),
     (2.84, 3.20, "Lundi,"), (3.43, 4.41, "tu te promets de commencer."),
     (5.17, 5.69, "Dimanche..."), (6.29, 6.84, "rien n'a bougé."),
     (7.81, 8.79, "Encore une semaine perdue."), (9.96, 11.13, "Ce n'est pas un manque de talent,"),
     (11.94, 12.37, "c'est une"), (12.53, 13.16, "petite voix."),
     (13.98, 15.18, "Et ce livre la démasque :"), (15.79, 17.09, "Plus malin que le diable."),
     (17.67, 18.81, "Tu vas reconnaître ses ruses,"), (19.38, 19.82, "lui répondre,"),
     (20.58, 22.37, "et passer enfin à l'action."), (23.14, 23.72, "En bonus :"), (24.18, 25.63, "Réfléchissez et devenez riche."),
     (26.60, 27.88, "Satisfait ou remboursé."), (28.70, 30.88, "Et tout ça pour seulement 990 F."),
     (31.60, 32.60, "Clique sur « Je le veux »."),
     (33.38, 35.12, "Ta prochaine semaine commence maintenant.")]
def weight(w):
    return max(1, len(re.findall(r"[aeiouyéèêàâîôûœ]+", w.lower()))) + 0.3
words, phrases = [], []
for s, e, text in P:
    toks = [t for t in text.replace(" ?", "?").replace("« ","«").replace(" »","»").replace(" :",":").split() if t]
    tot = sum(weight(t) for t in toks); t0 = s; idx = []
    for t in toks:
        d = (e - s) * weight(t) / tot
        idx.append(len(words)); words.append({"w": t, "s": round(t0, 2), "e": round(t0 + d, 2)}); t0 += d
    phrases.append({"start": s, "end": e, "text": text, "words": idx})
json.dump({"audio": "assets/audio/voix-montage.wav", "duration": 38.2, "phrases": phrases, "words": words},
          open(here / "onsets.json", "w"), ensure_ascii=False, indent=1)
json.dump({"duration": 38.2, "words": [{"w": x["w"], "start": x["s"], "end": x["e"]} for x in words]},
          open(here / "assets/audio/voix-montage-mots.json", "w"), ensure_ascii=False, indent=1)
print(len(words), "words")
