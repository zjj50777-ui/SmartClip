"""AI processing module - supports local LLM via Ollama."""

import requests


def call_ollama(prompt, model="qwen2.5:3b", host="http://localhost:11434"):
    """Call local Ollama API for text processing."""
    try:
        resp = requests.post(
            f"{host}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=30,
        )
        if resp.status_code == 200:
            return resp.json().get("response", "")
    except Exception:
        pass
    return None


def translate_text(text, target_lang="Chinese", model="qwen2.5:3b"):
    """Translate text using local LLM."""
    prompt = (
        f"Translate the following text to {target_lang}. "
        f"Output only the translation, no extra text:\n\n{text}"
    )
    return call_ollama(prompt, model=model)


def summarize_text(text, model="qwen2.5:3b"):
    """Summarize text using local LLM."""
    prompt = (
        "Summarize the following text in 2-3 concise sentences. "
        f"Output only the summary:\n\n{text}"
    )
    return call_ollama(prompt, model=model)


def format_code(text, model="qwen2.5:3b"):
    """Format and beautify code snippet using local LLM."""
    prompt = (
        "Reformat the following code with proper indentation and style. "
        "Output only the formatted code, no extra text:\n\n"
    ) + text
    return call_ollama(prompt, model=model)


def explain_code(text, model="qwen2.5:3b"):
    """Explain a code snippet in plain language."""
    prompt = (
        "Explain the following code in simple terms. "
        "Keep it under 100 words:\n\n"
    ) + text
    return call_ollama(prompt, model=model)
