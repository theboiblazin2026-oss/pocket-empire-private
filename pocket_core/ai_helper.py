"""
Pocket Empire — Centralized AI Helper
========================================
Single source of truth for all Google Gemini AI calls.
Uses the stable `google-genai` SDK (not the deprecated google-generativeai).
Includes: API key resolution, retry with backoff, and graceful fallbacks.

Usage:
    from pocket_core.ai_helper import ask_gemini, ask_gemini_with_image

    result = ask_gemini("Summarize this text...", api_key=optional_key)
    result = ask_gemini_with_image(image_bytes, "Analyze this receipt", "image/jpeg")
"""

import os
import time
import json

# ── Configuration ──────────────────────────────────────────────────────────
MODEL_NAME = "gemini-2.0-flash"  # Stable, long-lived model
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2  # Base delay, doubles each retry

# ── API Key Resolution ─────────────────────────────────────────────────────
def _resolve_api_key(api_key=None):
    """
    Resolve the Gemini API key from multiple sources (in priority order):
    1. Explicitly passed key
    2. Streamlit session state
    3. Streamlit secrets (multiple key names)
    4. Environment variable
    """
    if api_key:
        return api_key

    # Try Streamlit session state
    try:
        import streamlit as st
        key = st.session_state.get("GOOGLE_API_KEY")
        if key:
            return key
    except Exception:
        pass

    # Try Streamlit secrets (multiple possible key names)
    try:
        import streamlit as st
        for key_name in ["GOOGLE_API_KEY", "GEMINI_API_KEY"]:
            if key_name in st.secrets:
                return st.secrets[key_name]
        # Nested format: [gemini] api_key = "..."
        if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
            return st.secrets["gemini"]["api_key"]
    except Exception:
        pass

    # Try environment variable
    for env_name in ["GOOGLE_API_KEY", "GEMINI_API_KEY"]:
        val = os.environ.get(env_name)
        if val:
            return val

    return None


# ── Core: Text-only generation ─────────────────────────────────────────────
def ask_gemini(prompt, api_key=None, model=None):
    """
    Send a text prompt to Gemini and return the response text.
    Returns (text, None) on success, or (None, error_string) on failure.
    """
    resolved_key = _resolve_api_key(api_key)
    if not resolved_key:
        return None, "No API key found. Add your Google API Key in Settings."

    chosen_model = model or MODEL_NAME

    from google import genai
    client = genai.Client(api_key=resolved_key)

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=chosen_model,
                contents=prompt,
            )
            return response.text, None
        except Exception as e:
            last_error = str(e)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))

    return None, f"AI Error after {MAX_RETRIES} retries: {last_error}"


# ── Core: Image + text generation ──────────────────────────────────────────
def ask_gemini_with_image(image_bytes, prompt, mime_type="image/jpeg", api_key=None, model=None):
    """
    Send an image + text prompt to Gemini and return the response text.
    Returns (text, None) on success, or (None, error_string) on failure.
    """
    resolved_key = _resolve_api_key(api_key)
    if not resolved_key:
        return None, "No API key found. Add your Google API Key in Settings."

    chosen_model = model or MODEL_NAME

    from google import genai
    from google.genai import types
    client = genai.Client(api_key=resolved_key)

    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=chosen_model,
                contents=[image_part, prompt],
            )
            return response.text, None
        except Exception as e:
            last_error = str(e)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))

    return None, f"AI Error after {MAX_RETRIES} retries: {last_error}"


# ── Utility: Parse JSON from AI response ───────────────────────────────────
def parse_json_response(text):
    """
    Safely extract JSON from an AI response that may contain markdown fencing.
    Returns (parsed_dict_or_list, None) on success, or (None, error_string).
    """
    if not text:
        return None, "Empty response"

    cleaned = text.strip()
    # Strip markdown code fences
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned), None
    except json.JSONDecodeError as e:
        # Try to find JSON array or object within the text
        import re
        json_match = re.search(r'[\[{].*[}\]]', cleaned, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group()), None
            except json.JSONDecodeError:
                pass
        return None, f"Could not parse JSON: {e}"
