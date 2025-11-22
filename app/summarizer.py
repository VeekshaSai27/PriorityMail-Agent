# app/summarizer.py
"""
Summarize email body into a short plain-language explanation (2-3 sentences).
If Gemini/LLM is available, call it; fallback to first 1-2 sentences.
"""

import re

def _llm_summarize(body_text: str) -> str:
    """
future changes.....
    """
    return None  # placeholder, allow fallback

def summarize_email(body_text: str) -> str:
    if not body_text:
        return "No content to summarize."

    # Try LLM first (if available)
    try:
        llm_summary = _llm_summarize(body_text)
        if llm_summary:
            return llm_summary.strip()
    except Exception:
        pass

    # fallback: extract first two meaningful sentences
    # replace newlines with spaces, collapse whitespace
    text = re.sub(r'\s+', ' ', body_text).strip()
    # split into sentences (very simple)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if not sentences:
        return text[:200] + ("..." if len(text)>200 else "")

    # pick up to 2 sentences that are not very short
    out = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        out.append(s)
        if len(out) >= 2:
            break

    summary = " ".join(out)
    # short and plain
    if len(summary) > 400:
        summary = summary[:400].rsplit(" ", 1)[0] + "..."
    return summary
