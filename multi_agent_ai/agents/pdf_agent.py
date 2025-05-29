import fitz  # PyMuPDF
import re
from memory_manager import MemoryManager
import uuid

mem = MemoryManager()

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def detect_intent(text):
    # Basic intent detection based on keywords
    intents = {
        "Invoice": ["invoice", "amount due", "billing", "payment due", "total"],
        "Complaint": ["complaint", "issue", "problem", "not working", "damaged"],
        "RFQ": ["request for quotation", "quote", "pricing"],
        "Regulation": ["compliance", "regulation", "policy", "rule"],
    }
    text_lower = text.lower()
    for intent, keywords in intents.items():
        if any(keyword in text_lower for keyword in keywords):
            return intent
    return "General"

def extract_invoice_fields(text):
    # Example simple regex extraction, can be expanded
    invoice_number = re.search(r"Invoice Number[:\s]*([A-Za-z0-9\-]+)", text, re.IGNORECASE)
    date = re.search(r"Date[:\s]*([\d/.-]+)", text, re.IGNORECASE)
    total_amount = re.search(r"Total Amount[:\s]*\$?([\d,.]+)", text, re.IGNORECASE)
    
    return {
        "invoice_number": invoice_number.group(1) if invoice_number else None,
        "date": date.group(1) if date else None,
        "total_amount": total_amount.group(1) if total_amount else None,
    }

def process_pdf(file_path, source="unknown_source", conversation_id=None):
    text = extract_text_from_pdf(file_path)
    intent = detect_intent(text)
    extracted_fields = extract_invoice_fields(text)

    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    anomalies = [k for k, v in extracted_fields.items() if v is None]

    mem.log_entry(
        source=source,
        fmt="PDF",
        conversation_id=conversation_id,
        extracted_data={
            "intent": intent,
            "fields": extracted_fields,
            "anomalies": anomalies,
        },
    )

    return {
        "intent": intent,
        "fields": extracted_fields,
        "anomalies": anomalies,
        "conversation_id": conversation_id,
    }
