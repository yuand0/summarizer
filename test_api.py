#!/usr/bin/env python3
import os
import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.deepseek.com/v1")

def test_requests():
    if not API_KEY:
        print("❌ 请先设置 OPENAI_API_KEY")
        return False
    
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": "deepseek-chat",  # ← 改成 DeepSeek 模型
            "messages": [
                {"role": "system", "content": "请将以下文本摘要为不超过10个字。"},
                {"role": "user", "content": "这是一段中文测试文本，用于验证API调用是否正常工作。"}
            ],
            "temperature": 0.3,
            "max_tokens": 50
        }
        print(f"正在调用: {BASE_URL}/chat/completions")
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ API 调用成功:")
            print(f"   {result['choices'][0]['message']['content'].strip()}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:300]}")
            return False
    except Exception as e:
        print(f"❌ 调用失败: {e}")
        return False

if __name__ == "__main__":
    print("=== API 联调测试 ===\n")
    if test_requests():
        print("\n✅ API 联调正常")
    else:
        print("\n❌ API 联调失败")
