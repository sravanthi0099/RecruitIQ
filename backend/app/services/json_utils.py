"""Shared helper for extracting a JSON object from an LLM's raw text reply.

Why this exists: the previous approach in each *_service.py was
`text.find("{")` / `text.rfind("}")`, which grabs everything between the
FIRST '{' and the LAST '}' in the whole response. That's fine when the
model replies with nothing but the JSON object — but it silently returns
garbage the moment the model's reply contains extra braces anywhere
(e.g. echoing back part of the prompt, or wrapping the JSON in an
explanation). This scans for every balanced-brace substring and returns
the first one that actually parses, which is far more resilient.
"""

import json
import re


def extract_json(text: str) -> dict:
    if not text:
        return {"raw_response": text}

    cleaned = text.replace("```json", "").replace("```", "").strip()

    # Fast path: the whole reply is already valid JSON.
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # Scan for every balanced { ... } span and try each, preferring the
    # longest match first (most likely to be the intended full object).
    candidates = []
    stack = []
    start = None

    for i, ch in enumerate(cleaned):
        if ch == "{":
            if not stack:
                start = i
            stack.append(ch)
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack and start is not None:
                    candidates.append(cleaned[start:i + 1])

    # Try candidates in reverse order of appearance. LLMs that echo back
    # part of the prompt (e.g. restating candidate data) almost always do
    # so *before* giving their actual answer, so the last balanced JSON
    # blob in the text is the one we want -- not the longest one.
    for candidate in reversed(candidates):
        try:
            return json.loads(candidate)
        except Exception:
            continue

    # Last resort: the old naive approach, so we still return *something*.
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    return {"raw_response": cleaned}
