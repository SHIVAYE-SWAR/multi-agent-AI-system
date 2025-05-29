from memory_manager import MemoryManager
import uuid
import re

mem = MemoryManager()

def extract_sender(email_text):
    # Simple regex to extract email addresses from text
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', email_text)
    return emails[0] if emails else "unknown_sender"

def detect_urgency(email_text):
    # Basic keyword-based urgency detection
    urgency_keywords = {
        "high": ["urgent", "asap", "immediately", "important", "priority"],
        "low": ["whenever", "no rush", "not urgent", "no hurry"],
    }
    email_lower = email_text.lower()
    for level, keywords in urgency_keywords.items():
        if any(word in email_lower for word in keywords):
            return level.capitalize()
    return "Normal"

def detect_intent(email_text):
    # Basic intent detection by keyword
    intents = {
        "RFQ": ["request for quotation", "quote", "pricing", "cost"],
        "Complaint": ["complaint", "issue", "problem", "not satisfied"],
        "Invoice": ["invoice", "bill", "payment due", "amount owed"],
        "Regulation": ["compliance", "regulation", "policy", "rule"],
    }
    email_lower = email_text.lower()
    for intent, keywords in intents.items():
        if any(keyword in email_lower for keyword in keywords):
            return intent
    return "General"

def process_email(email_text, source="unknown_source", conversation_id=None):
    sender = extract_sender(email_text)
    urgency = detect_urgency(email_text)
    intent = detect_intent(email_text)

    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    extracted_data = {
        "sender": sender,
        "urgency": urgency,
        "intent": intent,
    }

    mem.log_entry(
        source=source,
        fmt="Email",
        conversation_id=conversation_id,
        extracted_data=extracted_data,
    )

    return {
        "sender": sender,
        "urgency": urgency,
        "intent": intent,
        "conversation_id": conversation_id,
    }
