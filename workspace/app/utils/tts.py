from app.api.tts import check_tts_loaded_model, check_tts_server_connection


def check_ready_tts_server():
    conn = check_tts_server_connection()
    model = check_tts_loaded_model()

    if conn == {"status": "no connection"}:
        return False

    if model == {"status": "no model"}:
        return False

    return True


def check_ready_for_load_model():
    conn = check_tts_server_connection()

    if conn == {"status": "no connection"}:
        return False

    return True
