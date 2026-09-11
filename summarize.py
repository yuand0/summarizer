import hashlib
from openai_summarize import summarize_text
from cache import get_cached_summary, set_cached_summary

def generate_summary(text: str, max_length: int = 100, use_mock: bool = False) -> dict:
    if not text or len(text.strip()) == 0:
        return {"error": "文本不能为空"}
    
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    
    if not use_mock:
        cached = get_cached_summary(text)
        if cached:
            cached["cached"] = True
            return cached
    
    if use_mock:
        summary = text[:max_length] + "..." if len(text) > max_length else text
        result = {"original_length": len(text), "summary": summary, "summary_length": len(summary), "text_hash": text_hash, "mock": True}
    else:
        try:
            summary = summarize_text(text, max_length)
            result = {"original_length": len(text), "summary": summary, "summary_length": len(summary), "text_hash": text_hash, "mock": False}
        except Exception as e:
            return {"error": f"API 调用失败: {str(e)}"}
    
    if not use_mock:
        set_cached_summary(text, result)
    
    return result
