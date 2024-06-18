import json
import os


def get_locale(language, cog):
    default_language = "en"
    file_path = f"locales/{language}.json"
    if not os.path.exists(file_path):
        file_path = f"locales/{default_language}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            locale_data = json.load(file)
            return locale_data.get(cog, {})
    return {}
