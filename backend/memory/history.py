history = {}

def get_history(session_id):
    return history.get(session_id, [])

def add_message(session_id, role, content):
    if session_id not in history:
        history[session_id] = []

    history[session_id].append({
        "role": role,
        "content": content
    })