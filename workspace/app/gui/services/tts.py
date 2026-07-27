from app.api.tts import get_models


class GetTTSModels:
    @staticmethod
    def get_list():
        models = get_models()
        result = list()

        if isinstance(models, str):
            print(f"{models = }")
            return

        for key, value in models.items():
            result.append(f"{key}|{value.get('name')}. {value.get('ckpt_path')}")

        return result
