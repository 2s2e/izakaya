def convert_history_to_string(history):
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
