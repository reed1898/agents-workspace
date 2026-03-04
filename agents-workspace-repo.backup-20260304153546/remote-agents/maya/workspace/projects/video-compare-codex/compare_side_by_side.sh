#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $(basename "$0") [--mute] [--label] <left_video> <right_video> <output_video>

Options:
  --mute    Output video without audio
  --label   Overlay LEFT/RIGHT labels on top corners
EOF
}

MUTE=0
LABEL=0
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mute) MUTE=1; shift ;;
    --label) LABEL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

if [[ ${#ARGS[@]} -ne 3 ]]; then
  usage
  exit 1
fi

LEFT="${ARGS[0]}"
RIGHT="${ARGS[1]}"
OUT="${ARGS[2]}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "❌ ffmpeg not found. Install: brew install ffmpeg" >&2
  exit 1
fi
if ! command -v ffprobe >/dev/null 2>&1; then
  echo "❌ ffprobe not found (included with ffmpeg)." >&2
  exit 1
fi
for f in "$LEFT" "$RIGHT"; do
  if [[ ! -f "$f" ]]; then
    echo "❌ Input file not found: $f" >&2
    exit 1
  fi
done

# Smallest height between two videos
H1=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$LEFT" | tr -d '\r')
H2=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$RIGHT" | tr -d '\r')
if [[ -z "$H1" || -z "$H2" ]]; then
  echo "❌ Failed to read input video dimensions." >&2
  exit 1
fi
if (( H1 < H2 )); then MIN_H=$H1; else MIN_H=$H2; fi

if [[ "$LABEL" -eq 1 ]]; then
  FILTER="[0:v]scale=-2:${MIN_H},setsar=1,drawtext=text='LEFT':x=20:y=20:fontsize=36:fontcolor=white:box=1:boxcolor=black@0.5[v0];[1:v]scale=-2:${MIN_H},setsar=1,drawtext=text='RIGHT':x=w-tw-20:y=20:fontsize=36:fontcolor=white:box=1:boxcolor=black@0.5[v1];[v0][v1]hstack=inputs=2[v]"
else
  FILTER="[0:v]scale=-2:${MIN_H},setsar=1[v0];[1:v]scale=-2:${MIN_H},setsar=1[v1];[v0][v1]hstack=inputs=2[v]"
fi

CMD=(ffmpeg -y -i "$LEFT" -i "$RIGHT" -filter_complex "$FILTER" -map "[v]" -shortest -c:v libx264 -preset fast -crf 18)
if [[ "$MUTE" -eq 1 ]]; then
  CMD+=( -an )
else
  CMD+=( -map 0:a? -c:a aac -b:a 192k )
fi
CMD+=( "$OUT" )

"${CMD[@]}"
echo "✅ Done: $OUT"
