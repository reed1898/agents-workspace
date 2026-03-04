#!/usr/bin/env python3
"""批量转录音频"""
import os
import sys
import subprocess
import urllib.request
import json

AUDIO_DIR = "/Users/rain/.openclaw/media/inbound"
PROCESSED_FILE = "/Users/rain/.openclaw/workspace/.transcribed-audio.txt"

def get_api_key():
    for rc_file in [os.path.expanduser("~/.zshrc"), os.path.expanduser("~/.bashrc")]:
        try:
            with open(rc_file, "r") as f:
                for line in f:
                    if "OPENAI_API_KEY" in line and "=" in line:
                        key = line.split("=")[1].strip().strip('"').strip("'")
                        if key.startswith("sk-"):
                            return key
        except:
            pass
    return None

OPENAI_API_KEY = get_api_key()

def transcribe_file(filepath):
    if not OPENAI_API_KEY:
        return None
    
    # 转换 WAV
    wav_path = filepath.replace('.ogg', '.wav')
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y", "-i", filepath,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav_path
    ], capture_output=True)
    
    if not os.path.exists(wav_path):
        return None
    
    # 调用 API
    url = "https://api.openai.com/v1/audio/transcriptions"
    with open(wav_path, 'rb') as f:
        audio_data = f.read()
    
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    # 使用正确的方式构建 multipart body
    body = b''
    body += b'--' + boundary.encode() + b'\r\n'
    body += f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(filepath)}"\r\nContent-Type: audio/ogg\r\n\r\n'.encode()
    body += audio_data + b'\r\n'
    body += b'--' + boundary.encode() + b'\r\n'
    body += b'Content-Disposition: form-data; name="model"\r\n\r\nwhisper-1\r\n'
    body += b'--' + boundary.encode() + b'--\r\n'
    
    req = urllib.request.Request(url, data=body)
    req.add_header('Authorization', f'Bearer {OPENAI_API_KEY}')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode())
            return data.get('text', '').strip()
    except Exception as e:
        print(f"  错误: {e}")
        return None
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

def main():
    processed = set()
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as fp:
            for line in fp:
                processed.add(line.strip())
    
    if not OPENAI_API_KEY:
        print("错误: 未找到 OPENAI_API_KEY")
        return
    
    new_count = 0
    for filename in os.listdir(AUDIO_DIR):
        if not filename.endswith('.ogg'):
            continue
        if filename in processed:
            continue
        
        audio_path = os.path.join(AUDIO_DIR, filename)
        print(f"转录: {filename}")
        
        transcript = transcribe_file(audio_path)
        
        if transcript:
            txt_path = audio_path.replace('.ogg', '.txt')
            with open(txt_path, 'w') as f:
                f.write(transcript)
            print(f"  -> {transcript}")
        else:
            print("  -> 转录失败")
        
        processed.add(filename)
        with open(PROCESSED_FILE, 'a') as fp:
            fp.write(filename + '\n')
        new_count += 1
    
    print(f"处理了 {new_count} 个文件")

if __name__ == "__main__":
    main()
