#!/bin/bash
# Régénère la voix off BIKINI SHOP avec Gemini TTS, puis la découpe et la place scène par scène.
#
# Pré-requis : la clé Gemini est dans l'environnement cloud (« Network secrets », hôte
# generativelanguage.googleapis.com, en-tête x-goog-api-key). Le proxy ajoute la vraie clé :
# GEMINI_API_KEY ci-dessous n'est qu'une valeur de remplissage pour l'outil HyperFrames.
#
# Le texte, la voix (Leda) et le ton sont dans assets/voice/request.json ; le texte découpé en
# phrases est dans assets/voice/lines.json (les deux doivent rester identiques).
# Offre gratuite Gemini : 3 requêtes par minute, d'où une seule prise pour tout le texte.
set -euo pipefail
cd "$(dirname "$0")/.."
SKILLS="${SKILLS:-../../.claude/skills}"
GEMINI_API_KEY="${GEMINI_API_KEY:-via-network-secret}" NODE_USE_ENV_PROXY=1 \
  node "$SKILLS/media-use/audio/scripts/audio.mjs" \
  --request assets/voice/request.json --hyperframes . --out .hyperframes/vo_meta.json --only tts
python3 tools/split_voiceover.py
echo "Reporte les départs de assets/voice/plan.json dans index.html (<audio id=\"vo-NN\" data-start data-duration>),"
echo "puis relance la découpe de la musique : node $SKILLS/hyperframes-audio/scripts/carve.mjs --comp index.html"
