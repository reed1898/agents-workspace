#!/usr/bin/env bash
set -euo pipefail

INF=${INF:-/home/ubuntu/.local/bin/infsh}
MODEL=${MODEL:-google/veo-3-1-fast}
OUTDIR=${OUTDIR:-/tmp/openclaw/video-catpaw}
mkdir -p "$OUTDIR"

run() {
  local shot_id="$1"
  local prompt="$2"
  local duration="$3"
  local out="$OUTDIR/${shot_id}.json"

  "$INF" app run "$MODEL" --input "{\"prompt\": \"$prompt\", \"duration\": $duration}" --json --save "$out"
  echo "saved: $out"
}

# NOTE: Make sure you've logged in first: infsh login
run shot1 "A bright and clean warm kitchen countertop. Ultra close-up of a cute cartoon cat-paw steaming bowl fixed in center frame. Thick black sesame slurry, silky and glossy, pours into the bowl. Gentle natural window light, cinematic food macro, realistic texture, cozy Chinese New Year ambiance in background decorations. Keep bowl position stable." 3

run shot2 "Same kitchen and same cat-paw bowl in exactly the same position. Creamy white rice slurry pours into the bowl, smooth and silky, layering with black sesame base. Slight push-in compared to previous shot. Food commercial quality, macro realism." 3

run shot3 "Same bowl and same position, even closer. One to two clear fresh pear juice droplets fall into the cat-paw bowl and ripple softly. Progressive push-in, macro lens look, clean highlights, warm cozy kitchen background bokeh." 3

run shot4a "A wooden bamboo steamer lid is lifted, steam blooms and clears, revealing a cute cat-paw shaped black sesame rice cake inside. Warm, appetizing, bright kitchen lighting, natural steam motion." 3

run shot4b "Several black sesame rice cakes tumble from off-screen into a clean rustic bamboo steamer basket, then bounce twice to show chewy springy texture. Food ad style, crisp details, soft warm light." 3

run shot5 "Only a 5-year-old child's small hands, no face, wearing winter festive sleeves with Chinese New Year style, raise one black sesame cat-paw rice cake and gently twist it. Bright clean warm kitchen backdrop. Keep child identity unrecognizable." 3

echo "Done. Check JSON outputs under: $OUTDIR"
