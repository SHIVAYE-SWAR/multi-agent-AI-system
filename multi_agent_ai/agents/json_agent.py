from memory_manager import MemoryManager
import uuid

mem = MemoryManager()

# Define required fields and their types
TARGET_SCHEMA = {
    "vendor": str,
    "product_id": str,
    "quantity": int,
    "price_per_unit": float,
    "delivery_date": str,
}

def validate_and_reformat(json_payload):
    anomalies = []
    reformatted = {}

    for field, field_type in TARGET_SCHEMA.items():
        value = json_payload.get(field)
        if value is None:
            anomalies.append(f"Missing field: {field}")
            reformatted[field] = None
        else:
            # Type check (basic)
            if not isinstance(value, field_type):
                anomalies.append(f"Incorrect type for {field}: Expected {field_type.__name__}, got {type(value).__name__}")
                # Attempt to coerce or keep original value
                reformatted[field] = value
            else:
                reformatted[field] = value

    return reformatted, anomalies

def process_json(json_payload, source="unknown_source", conversation_id=None):
    reformatted, anomalies = validate_and_reformat(json_payload)

    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    mem.log_entry(
        source=source,
        fmt="JSON",
        conversation_id=conversation_id,
        extracted_data={
            "reformatted_data": reformatted,
            "anomalies": anomalies,
        }
    )

    return {
        "reformatted_data": reformatted,
        "anomalies": anomalies,
        "conversation_id": conversation_id,
    }
