#!/usr/bin/env python3
"""转录音频文件（支持中文）"""
import sys
import json
import subprocess

API_KEY = "8d431164fb33686578de27a1eb3d51fa64c41af5"
FFMPEG = "/opt/homebrew/bin/ffmpeg"

def transcribe_with_ffmpeg(filepath):
    """使用 ffmpeg + Deepgram general 模型"""
    wav_path = filepath.replace('.ogg', '.wav')
    
    # 转换
    result = subprocess.run([
        FFMPEG, '-y', '-i', filepath, 
        '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', wav_path
    ], capture_output=True)
    
    if result.returncode != 0:
        print(f"转换失败")
        return None
    
    # 调用 Deepgram
    import urllib.request
    
    url = "https://api.deepgram.com/v1/listen?model=2-general"
    
    with open(wav_path, 'rb') as f:
        audio_data = f.read()
    
    req = urllib.request.Request(url, data=audio_data)
    req.add_header('Authorization', f'Token {API_KEY}')
    req.add_header('Content-Type', 'audio/wav')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            transcript = data['results']['channels'][0]['alternatives'][0]['transcript']
            print(transcript if transcript else '(无法识别)')
    except Exception as e:
        print(f"错误: {e}")
    finally:
        import os
        if os.path.exists(wav_path):
            os.remove(wav_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        transcribe_with_ffmpeg(sys.argv[1])
    else:
        print("用法: python3 transcribe.py <音频文件路径>")
