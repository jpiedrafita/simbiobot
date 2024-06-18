import json
import os
import sys
from config import cfg
from common.logger import logger


def get_locale(language, cog):
    default_language = "en"
    file_path = f"{cfg.locales_path}{language}.json"
    if not os.path.exists(file_path):
        file_path = f"{cfg.locales_path}{default_language}.json"
    try:
        with open(file_path, "r") as file:
            locale_data = json.load(file)
            return locale_data.get(cog, {})
    except FileNotFoundError:
        logger.Error(f"Locale file not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.Error(f"Error reading locale file: {file_path}")
        sys.exit(1)


def get_aliases(cog):
    try:
        with open(cfg.aliases_file, "r") as file:
            aliases = json.load(file)
            return aliases.get(cog, {})
    except FileNotFoundError:
        logger.error(f"Aliases file not found: {cfg.aliases_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f"Error reading aliases file: {cfg.aliases_file}")
        sys.exit(1)
