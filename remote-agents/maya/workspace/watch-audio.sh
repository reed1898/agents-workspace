#!/bin/bash
# 自动转录 Telegram 语音消息
# 监视 /Users/rain/.openclaw/media/inbound 目录中的新 .ogg 文件

WATCH_DIR="/Users/rain/.openclaw/media/inbound"
API_KEY="8d431164fb33686578de27a1eb3d51fa64c41af5"
LOG_FILE="/Users/rain/.openclaw/workspace/transcribe.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "开始监视语音文件..."

# 获取已处理的文件列表
PROCESSED_FILE="/Users/rain/.openclaw/workspace/.processed-audio.txt"
touch "$PROCESSED_FILE"

while true; do
    for ogg_file in "$WATCH_DIR"/*.ogg; do
        [ -f "$ogg_file" ] || continue
        
        filename=$(basename "$ogg_file")
        
        # 检查是否已处理
        if grep -q "$filename" "$PROCESSED_FILE" 2>/dev/null; then
            continue
        fi
        
        log "发现新语音文件: $filename"
        
        # 转换为 WAV
        wav_file="${ogg_file%.ogg}.wav"
        if ffmpeg -y -i "$ogg_file" -ar 16000 -ac 1 -c:a pcm_s16le "$wav_file" 2>/dev/null; then
            # 调用 Deepgram 转录
            transcript=$(curl -s -X POST "https://api.deepgram.com/v1/listen?model=2-general" \
                -H "Authorization: Token $API_KEY" \
                -H "Content-Type: audio/wav" \
                --data-binary @"$wav_file" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data['results']['channels'][0]['alternatives'][0]['transcript'])
except:
    print('(转录失败)')
" 2>/dev/null)
            
            if [ -n "$transcript" ]; then
                log "转录结果: $transcript"
                
                # 保存转录结果
                transcript_file="${ogg_file%.ogg}.txt"
                echo "$transcript" > "$transcript_file"
                
                # 标记为已处理
                echo "$filename" >> "$PROCESSED_FILE"
                
                log "完成: $filename -> $transcript_file"
            fi
            
            # 清理临时 WAV 文件
            rm -f "$wav_file"
        fi
    done
    
    sleep 5
done
