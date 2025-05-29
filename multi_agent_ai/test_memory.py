# test_memory.py
from memory_manager import MemoryManager


def test_memory_module():
    mem = MemoryManager()

    mem.log_entry(
        source="vendor@example.com",
        fmt="Email",
        conversation_id="conv_12345",
        extracted_data={"intent": "RFQ", "urgency": "High", "sender": "vendor@example.com"}
    )

    entries = mem.get_conversation_entries("conv_12345")
    for e in entries:
        print(e)

    mem.close()

if __name__ == "__main__":
    test_memory_module()
