from app.api.tts import convert_audio_with_remote_session, get_models, load_model


def conveyor_models():
    models = get_models()
    print(models)

    for id, value in models.items():
        # print(id, type(id), value)
        load_model(id=int(id))
        convert_audio_with_remote_session(start_with=9890)
