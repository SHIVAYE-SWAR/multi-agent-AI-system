import sys
import json
from agents.classifier_agent import classify_input
from agents.pdf_agent import process_pdf
from agents.json_agent import process_json
from agents.email_agent import process_email

def main(input_data, input_type=None):
    # Step 1: Classify input format and intent
    classification = classify_input(input_data)
    fmt = classification.get("format")
    intent = classification.get("intent")
    print(f"Format Detected: {fmt}")
    print(f"Intent Detected: {intent}")

    # Step 2: Route to correct agent
    if fmt == "PDF":
        # input_data is expected to be a file path
        result = process_pdf(input_data, source="unknown")
    elif fmt == "JSON":
        # input_data is expected to be a dict or JSON string
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        result = process_json(input_data)
    elif fmt == "Email":
        # input_data is expected to be raw email text
        result = process_email(input_data)
    else:
        print("Unknown format. Cannot process.")
        return

    # Step 3: Output the processed result and conversation id
    print("Processed Result:", result)
    print("Conversation ID:", result.get("conversation_id"))

if __name__ == "__main__":
    # Example: Run with command line argument for PDF file
    # python main.py samples/sample.pdf

    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file_or_text>")
        sys.exit(1)

    input_arg = sys.argv[1]

    # Basic check to route: if ends with .pdf, treat as PDF file
    if input_arg.lower().endswith(".pdf"):
        main(input_arg)
    else:
        # Otherwise treat as text input - could be JSON or Email
        try:
            data = json.loads(input_arg)
            main(data)
        except json.JSONDecodeError:
            main(input_arg)
