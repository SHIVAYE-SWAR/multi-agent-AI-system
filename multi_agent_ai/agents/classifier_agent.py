# classifier_agent.py

import json
from utils.llm_utils import call_llm
from agents.pdf_agent import extract_text_from_pdf


def detect_format(input_data):
    """
    Detect the format of the input data.
    Returns one of: PDF, JSON, Email, Text, Unknown
    """
    if isinstance(input_data, dict):
        return "JSON"
    elif isinstance(input_data, str):
        # Heuristic for email detection
        if "From:" in input_data and "Subject:" in input_data:
            return "Email"
        elif input_data.lower().endswith(".pdf"):
            return "PDF"
        else:
            return "Text"
    elif isinstance(input_data, bytes):
        # You could add PDF signature detection here
        return "PDF"
    else:
        return "Unknown"


def detect_intent(text):
    """
    Use a local LLM (via Ollama) to determine the intent of the content.
    Returns one of: Invoice, RFQ, Complaint, Regulation, Other
    """
    prompt = f"""
You are a strict classifier. Read the following text and classify it into one of the following intents:

[Invoice, RFQ, Complaint, Regulation, Other]

Return your answer in **this exact JSON format**:
{{"intent": "<one of the 5 options>"}}

Text:
\"\"\"
{text[:1000]}
\"\"\"
"""
    try:
        raw_output = call_llm(prompt)
        # Parse LLM output safely
        parsed = json.loads(raw_output)
        return parsed.get("intent", "Other").strip()
    except Exception as e:
        print("Intent parsing failed:", e)
        return "Other"


def classify(input_data):
    """
    Main classification function.
    Returns a dictionary with detected format and intent.
    """
    fmt = detect_format(input_data)

    # Convert to string for intent detection
    intent_text = (
        json.dumps(input_data) if fmt == "JSON" else str(input_data)
    )

    intent = detect_intent(intent_text)

    return {
        "format": fmt,
        "intent": intent
    }

from memory_manager import MemoryManager

mem = MemoryManager()
import uuid

import os
import uuid
from utils.llm_utils import call_llm  # Your Ollama wrapper

def classify_input(input_data):
    # Format detection (basic)
    if isinstance(input_data, str):
        if os.path.exists(input_data) and input_data.lower().endswith(".pdf"):
            detected_format = "PDF"
            with open(input_data, "rb") as f:
                text = extract_text_from_pdf(input_data)
        elif input_data.strip().startswith("{"):
            detected_format = "JSON"
            text = input_data
        else:
            detected_format = "Email"
            text = input_data
    elif isinstance(input_data, dict):
        detected_format = "JSON"
        text = str(input_data)
    else:
        detected_format = "Unknown"
        text = ""

    # Intent detection using LLM
    prompt = f"Classify the intent of this message:\n\n{text}\n\nIntent:"
    intent_response = call_llm(prompt).strip()
    intent = intent_response.split("\n")[0] if intent_response else "General"

    return {"format": detected_format, "intent": intent}
