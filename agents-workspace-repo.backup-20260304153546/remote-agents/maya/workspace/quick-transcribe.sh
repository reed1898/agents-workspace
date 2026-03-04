#!/bin/bash
# 快速转录音频 - 支持中文
# 用法: bash ~/openclaw/workspace/quick-transcribe.sh <完整路径>

curl -s -X POST "https://api.deepgram.com/v1/listen?model=2-general" \
  -H "Authorization: Token 8d431164fb33686578de27a1eb3d51fa64c41af5" \
  -H "Content-Type: audio/ogg" \
  --data-binary @"$1" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    transcript = data['results']['channels'][0]['alternatives'][0]['transcript']
    print(transcript if transcript else '(无法识别)')
except Exception as e:
    print(f'错误: {e}')
"
