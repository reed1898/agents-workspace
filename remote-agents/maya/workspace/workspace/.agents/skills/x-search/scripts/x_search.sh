#!/bin/bash
# X Search via xAI Grok API
# Usage: x_search.sh "search query" [options]
# Options: --from-date YYYY-MM-DD --to-date YYYY-MM-DD --allowed-handles handle1,handle2 --excluded-handles handle1,handle2 --enable-images --enable-videos --thinking --max-tokens N

set -euo pipefail

if [ -z "${XAI_API_KEY:-}" ]; then
    echo "Error: XAI_API_KEY environment variable not set" >&2
    exit 1
fi

API_HOST="${XAI_API_HOST:-https://api.x.ai}"
MODEL="grok-4-1-fast-non-reasoning"
MAX_OUTPUT_TOKENS="280"
QUERY=""
TOOL_CONFIG='{"type": "x_search"'
PARAMS_ADDED=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --from-date)
            TOOL_CONFIG="${TOOL_CONFIG}, \"from_date\": \"$2\""
            PARAMS_ADDED=true
            shift 2
            ;;
        --to-date)
            TOOL_CONFIG="${TOOL_CONFIG}, \"to_date\": \"$2\""
            PARAMS_ADDED=true
            shift 2
            ;;
        --allowed-handles)
            HANDLES=$(echo "$2" | jq -R 'split(",") | map(. | @json) | join(", ")')
            TOOL_CONFIG="${TOOL_CONFIG}, \"allowed_x_handles\": [${HANDLES}]"
            PARAMS_ADDED=true
            shift 2
            ;;
        --excluded-handles)
            HANDLES=$(echo "$2" | jq -R 'split(",") | map(. | @json) | join(", ")')
            TOOL_CONFIG="${TOOL_CONFIG}, \"excluded_x_handles\": [${HANDLES}]"
            PARAMS_ADDED=true
            shift 2
            ;;
        --enable-images)
            TOOL_CONFIG="${TOOL_CONFIG}, \"enable_image_understanding\": true"
            PARAMS_ADDED=true
            shift
            ;;
        --enable-videos)
            TOOL_CONFIG="${TOOL_CONFIG}, \"enable_video_understanding\": true"
            PARAMS_ADDED=true
            shift
            ;;
        --thinking)
            MODEL="grok-4-1-fast-reasoning"
            shift
            ;;
        --max-tokens)
            MAX_OUTPUT_TOKENS="$2"
            shift 2
            ;;
        *)
            QUERY="$1"
            shift
            ;;
    esac
done

TOOL_CONFIG="${TOOL_CONFIG}}"

if [ -z "$QUERY" ]; then
    echo "Error: Search query required" >&2
    exit 1
fi

PAYLOAD=$(cat <<EOF
{
  "model": "$MODEL",
  "max_output_tokens": $MAX_OUTPUT_TOKENS,
  "input": [
    {
      "role": "user",
      "content": "$QUERY"
    }
  ],
  "tools": [
    $TOOL_CONFIG
  ]
}
EOF
)

RESPONSE=$(curl -s "${API_HOST}/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${XAI_API_KEY}" \
  -d "$PAYLOAD")

# Parse and display the response (robust to missing/non-numeric citation titles)
echo "$RESPONSE" | jq -r '
  .output[-1].content[0] as $content |

  # Extract text
  ($content.text // "No response text found") as $text |

  # Extract unique citations and sort safely
  ($content.annotations // []
   | map(select(.type == "url_citation" and (.url != null)))
   | unique_by(.url)
   | sort_by((.title // "")|tostring)
   | map("[\((.title // "ref")|tostring)] \(.url)")
   | join("\n")) as $citations |

  # Format output
  "## Response\n\n" + $text +
  (if $citations != "" then "\n\n## Citations\n" + $citations else "" end)
'
