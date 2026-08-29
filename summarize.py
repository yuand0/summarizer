import hashlib
from openai_summarize import summarize_text

def generate_summary(text: str, max_length: int = 100, use_mock: bool = False) -> dict:
    """
    生成摘要
    use_mock=True: 使用 mock 模式（不消耗 API 额度）
    use_mock=False: 调用真实 DeepSeek API
    """
    if not text or len(text.strip()) == 0:
        return {"error": "文本不能为空"}
    
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    
    if use_mock:
        # Mock 模式
        if len(text) <= max_length:
            summary = text
        else:
            summary = text[:max_length] + "..."
        return {
            "original_length": len(text),
            "summary": summary,
            "summary_length": len(summary),
            "text_hash": text_hash,
            "mock": True
        }
    else:
        # 真实 API 模式
        try:
            summary = summarize_text(text, max_length)
            return {
                "original_length": len(text),
                "summary": summary,
                "summary_length": len(summary),
                "text_hash": text_hash,
                "mock": False
            }
        except Exception as e:
            return {"error": f"API 调用失败: {str(e)}"}
