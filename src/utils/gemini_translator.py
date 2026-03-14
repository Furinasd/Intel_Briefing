"""
Gemini Translator - 使用 Gemini API 翻译文本为中文
用于将 ArXiv 论文摘要翻译成简体中文
"""
import sys
import time
import logging
import httpx

logger = logging.getLogger(__name__)

# Force UTF-8 stdout for Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import from centralized config
try:
    from config import GEMINI_API_KEY, GEMINI_API_URL, GEMINI_MODEL, GEMINI_TIMEOUT, GEMINI_MAX_RETRIES
except ImportError:
    from src.config import GEMINI_API_KEY, GEMINI_API_URL, GEMINI_MODEL, GEMINI_TIMEOUT, GEMINI_MAX_RETRIES

def _gemini_api_call(prompt: str, max_tokens: int = 1024) -> str:
    """内部通用函数：处理不同类型的 Gemini API 调用。"""
    if not GEMINI_API_KEY:
        return ""

    # Determine URL and headers
    if GEMINI_API_URL.endswith("/chat/completions") or "v1/chat" in GEMINI_API_URL:
        # OpenAI-compatible endpoint
        url = GEMINI_API_URL
        headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
        payload = {
            "model": GEMINI_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
        api_type = "openai"
    else:
        # Google-style endpoint
        base_url = GEMINI_API_URL.rstrip("/")
        if "/models" not in base_url and "v1" not in base_url:
            base_url = f"{base_url}/v1beta/models"
        
        url = f"{base_url}/{GEMINI_MODEL}:generateContent"
        
        headers = {}
        if GEMINI_API_KEY.startswith("sk-"):
            headers["Authorization"] = f"Bearer {GEMINI_API_KEY}"
            api_type = "google_proxy"
        else:
            url += f"?key={GEMINI_API_KEY}"
            api_type = "google_direct"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": max_tokens
            }
        }

    for attempt in range(GEMINI_MAX_RETRIES):
        try:
            response = httpx.post(url, json=payload, headers=headers, timeout=GEMINI_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            if api_type == "openai":
                result = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                result = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            if result:
                return result.strip()
            
            if attempt < GEMINI_MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
                continue
        except Exception as e:
            if hasattr(e, 'response') and e.response is not None:
                logger.warning(f"Gemini API Error Response: {e.response.text}")
            if attempt < GEMINI_MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
                continue
            logger.error(f"Gemini API 最终失败: {e}")
    return ""

def translate_to_chinese(text: str, max_chars: int = 100) -> str:
    """将英文文本翻译成简体中文。"""
    if not text or len(text) < 10:
        return text
    
    prompt = f"请将以下学术论文摘要完整翻译成简体中文，要求：\n1. 保持学术风格，用词精准\n2. 完整翻译全部内容\n3. 只输出翻译结果\n\n原文：\n{text}"
    
    result = _gemini_api_call(prompt)
    if result:
        return result
    return text[:max_chars] + "..." if len(text) > max_chars else text
    
    return text[:max_chars] + "..." if len(text) > max_chars else text


def translate_summary_pair(summary: str) -> tuple[str, str]:
    """
    为 ArXiv 论文生成两层摘要（中文）。
    
    Args:
        summary: 英文原始摘要
    
    Returns:
        (brief_cn, detail_cn) - 短摘要和详细摘要的中文版本
    """
    if not summary:
        return ("", "")
    
    # Brief: 翻译前100字
    brief_cn = translate_to_chinese(summary[:200], max_chars=80)
    
    # Detail: 翻译完整摘要
    detail_cn = translate_to_chinese(summary, max_chars=500)
    
    return (brief_cn, detail_cn)


def summarize_blog_article(content: str, mode: str = "brief") -> str:
    """为技术博客文章生成情报简报风格的中文摘要。"""
    if not GEMINI_API_KEY or not content or len(content) < 50:
        return ""
    
    if mode == "brief":
        prompt = f"请阅读以下技术博客文章，用一句话中文概括核心观点（最多100字）。直接说重点。\n\n内容：\n{content[:2000]}"
        max_tokens = 256
    else:
        prompt = f"请作为技术情报分析师，阅读以下博客文章并生成中文深度分析报告（背景、发现、细节、价值）。总长度 300-500 字。\n\n内容：\n{content[:6000]}"
        max_tokens = 1024
    
    return _gemini_api_call(prompt, max_tokens=max_tokens)


if __name__ == "__main__":
    # Test translation
    test_text = "Adapting large pretrained models to new tasks efficiently and continually is crucial for real-world deployment but remains challenging due to catastrophic forgetting."
    print("原文:", test_text)
    print("翻译:", translate_to_chinese(test_text, 80))
