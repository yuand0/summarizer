import os
import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.deepseek.com/v1")

def summarize_text(text: str, max_length: int = 100) -> str:
    if not text or len(text.strip()) == 0:
        raise ValueError("文本不能为空")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": f"请将以下文本摘要为不超过{max_length}字，只返回摘要内容。"},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3,
        "max_tokens": max_length * 2
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"API 返回错误: {response.status_code} - {response.text[:200]}")
    
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()
