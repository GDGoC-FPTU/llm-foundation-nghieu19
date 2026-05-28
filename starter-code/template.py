"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Estimated costs per 1M INPUT & OUTPUT tokens (USD) as of March 2026
# Vietnamese text generally consumes ~1.5x - 2.0x more tokens than English due to Unicode/diacritics.
# ---------------------------------------------------------------------------
PRICING_1M_TOKENS = {
    "gpt-4o": {"input": 5.00, "output": 20.00},
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.300},
    "gemini-2.5-pro": {"input": 1.25, "output": 5.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
}

# Standard Model Identifiers
OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"
GEMINI_MODEL = "gemini-2.5-flash"
ANTHROPIC_MODEL = "claude-3-5-haiku"


# ---------------------------------------------------------------------------
# Task 1 — Call OpenAI (GPT-4o)
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:
    from openai import OpenAI
 
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start
 
    response_text = response.choices[0].message.content
    usage = {
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
    }
 
    return response_text, latency, usage


# ---------------------------------------------------------------------------
# Task 2 — Call Google Gemini 2.5 (Standard Practical Model)
# ---------------------------------------------------------------------------
def call_gemini(
    prompt: str,
    model: str = GEMINI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:
    from google import genai
    from google.genai import types
 
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
 
    config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_tokens,
    )
 
    start = time.time()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    latency = time.time() - start
 
    response_text = response.text
    usage = {
        "input_tokens": response.usage_metadata.prompt_token_count,
        "output_tokens": response.usage_metadata.candidates_token_count,
    }
 
    return response_text, latency, usage

# ---------------------------------------------------------------------------
# Task 3 — Call Anthropic Claude (Exploratory track)
# ---------------------------------------------------------------------------
def call_anthropic(
    prompt: str,
    model: str = ANTHROPIC_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:
    import anthropic
 
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
 
    start = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = time.time() - start
 
    response_text = response.content[0].text
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
 
    return response_text, latency, usage
# ---------------------------------------------------------------------------
# Task 4 — Compare Models (OpenAI GPT-4o vs OpenAI Mini vs Gemini 2.5 Flash)
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    def calc_cost(model_key: str, input_tokens: int, output_tokens: int) -> float:
        pricing = PRICING_1M_TOKENS[model_key]
        return (
            input_tokens  * pricing["input"]  +
            output_tokens * pricing["output"]
        ) / 1_000_000
 
    # ── gpt-4o ──
    text_4o, lat_4o, usage_4o = call_openai(prompt, model=OPENAI_MODEL)
    cost_4o = calc_cost("gpt-4o", usage_4o["input_tokens"], usage_4o["output_tokens"])
 
    # ── gpt-4o-mini ──
    text_mini, lat_mini, usage_mini = call_openai(prompt, model=OPENAI_MINI_MODEL)
    cost_mini = calc_cost("gpt-4o-mini", usage_mini["input_tokens"], usage_mini["output_tokens"])
 
    # ── gemini-2.5-flash ──
    text_gem, lat_gem, usage_gem = call_gemini(prompt, model=GEMINI_MODEL)
    cost_gem = calc_cost("gemini-2.5-flash", usage_gem["input_tokens"], usage_gem["output_tokens"])
 
    return {
        "gpt4o": {
            "response"     : text_4o,
            "latency"      : lat_4o,
            "cost"         : cost_4o,
            "input_tokens" : usage_4o["input_tokens"],
            "output_tokens": usage_4o["output_tokens"],
        },
        "gpt4o_mini": {
            "response"     : text_mini,
            "latency"      : lat_mini,
            "cost"         : cost_mini,
            "input_tokens" : usage_mini["input_tokens"],
            "output_tokens": usage_mini["output_tokens"],
        },
        "gemini_flash": {
            "response"     : text_gem,
            "latency"      : lat_gem,
            "cost"         : cost_gem,
            "input_tokens" : usage_gem["input_tokens"],
            "output_tokens": usage_gem["output_tokens"],
        },
    }
# ---------------------------------------------------------------------------
# Task 5 — Streaming chatbot with Gemini 2.5 (Focus Model)
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    from google import genai
    from google.genai import types
 
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    history: list[dict] = []  # {"role": "user"|"model", "parts": [{"text": "..."}]}
 
    print(f"\n🤖  Gemini 2.5 Flash Chatbot  (gõ 'exit' hoặc 'quit' để thoát)\n")
    print("─" * 60)
 
    while True:
        try:
            user_input = input("\nBạn: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋  Tạm biệt!")
            break
 
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("\n👋  Tạm biệt!")
            break
 
        
        history.append({"role": "user", "parts": [{"text": user_input}]})
 
        
        history = history[-6:]
 
        
        formatted_history = [
            types.Content(
                role=msg["role"],
                parts=[types.Part(text=p["text"]) for p in msg["parts"]],
            )
            for msg in history
        ]
 
        # Streaming response
        print("\nGemini: ", end="", flush=True)
        full_reply = ""
 
        try:
            response_stream = client.models.generate_content_stream(
                model=GEMINI_MODEL,
                contents=formatted_history,
            )
            for chunk in response_stream:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_reply += chunk.text
        except Exception as e:
            print(f"\n⚠️  Lỗi API: {e}")
            history.pop()  
            continue
 
        print()  
 
        # Thêm reply của model vào history
        history.append({"role": "model", "parts": [{"text": full_reply}]})
        history = history[-6:]
# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable[[], Any],
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    last_exception = None
 
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
 
    raise last_exception

# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    results = []
    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)
    return results

# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format batch_compare results as a Markdown table.
 
    Columns: Prompt | Model | Response (truncated) | Latency | Tokens (In/Out) | Cost (USD)
    """
    header = (
        "| Prompt | Model | Response | Latency | Tokens (In/Out) | Cost (USD) |\n"
        "|--------|-------|----------|---------|-----------------|------------|"
    )
 
    MODEL_LABELS = {
        "gpt4o"       : "GPT-4o",
        "gpt4o_mini"  : "GPT-4o Mini",
        "gemini_flash": "Gemini 2.5 Flash",
    }
 
    rows = []
    for result in results:
        prompt_short = result.get("prompt", "")[:40].replace("|", "\\|")
        if len(result.get("prompt", "")) > 40:
            prompt_short += "…"
 
        for key, label in MODEL_LABELS.items():
            if key not in result:
                continue
            stats = result[key]
            response_short = stats["response"][:50].replace("|", "\\|").replace("\n", " ")
            if len(stats["response"]) > 50:
                response_short += "…"
 
            rows.append(
                f"| {prompt_short} "
                f"| {label} "
                f"| {response_short} "
                f"| {stats['latency']:.2f}s "
                f"| {stats['input_tokens']} / {stats['output_tokens']} "
                f"| ${stats['cost']:.6f} |"
            )
 
    return header + "\n" + "\n".join(rows)

# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Model Comparison Test ===")
    test_prompt = "Hãy giải thích sự khác biệt giữa temperature và top_p bằng tiếng Việt ngắn gọn trong 2 câu."
    try:
        # Note: Requires valid API keys set in environment variables
        result = compare_models(test_prompt)
        for model_name, stats in result.items():
            print(f"\n[{model_name.upper()}]")
            print(f"Latency: {stats['latency']:.2f}s | Cost: ${stats['cost']:.6f}")
            print(f"Tokens: {stats['input_tokens']} in / {stats['output_tokens']} out")
            print(f"Response: {stats['response']}")
    except Exception as e:
        print(f"Skipping live API comparison test: {e}")
        print("Set your API keys to run manual tests.")

    print("\n=== Starting Gemini 2.5 Chatbot (type 'quit' to exit) ===")
    try:
        streaming_chatbot()
    except Exception as e:
        print(f"Chatbot failed to start: {e}")
