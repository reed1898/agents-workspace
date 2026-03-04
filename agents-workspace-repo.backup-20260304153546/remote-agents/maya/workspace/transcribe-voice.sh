#!/bin/bash
# 转录 Telegram 语音消息
# 用法: ./transcribe-voice.sh <文件名>

API_KEY="8d431164fb33686578de27a1eb3d51fa64c41af5"
AUDIO_DIR="/Users/rain/.openclaw/media/inbound"

if [ -z "$1" ]; then
    # 转录所有文件
    for f in "$AUDIO_DIR"/*.ogg; do
        if [ -f "$f" ]; then
            filename=$(basename "$f")
            echo "=== $filename ==="
            result=$(curl -s -X POST "https://api.deepgram.com/v1/listen?model=nova-3&language=zh" \
                -H "Authorization: Token $API_KEY" \
                -H "Content-Type: audio/ogg" \
                --data-binary @"$f")
            transcript=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin)['results']['channels'][0]['alternatives'][0]['transcript'])" 2>/dev/null)
            echo "$transcript"
            echo ""
        fi
    done
else
    # 转录指定文件
    f="$AUDIO_DIR/$1"
    if [ -f "$f" ]; then
        result=$(curl -s -X POST "https://api.deepgram.com/v1/listen?model=nova-3&language=zh" \
            -H "Authorization: Token $API_KEY" \
            -H "Content-Type: audio/ogg" \
            --data-binary @"$f")
        transcript=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin)['results']['channels'][0]['alternatives'][0]['transcript'])" 2>/dev/null)
        echo "$transcript"
    else
        echo "文件不存在: $f"
    fi
fi
