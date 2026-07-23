from app.api.tts import streaming_conversion, get_models, load_model


def conveyor_models():
    models = get_models()
    print(models)

    for id, value in models.items():
        # print(id, type(id), value)
        load_model(id=int(id))
        streaming_conversion(start_with=9890)
