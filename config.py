import os
from box import Box
from ruamel.yaml import YAML
from dotenv import load_dotenv
from common.logger import logger

load_dotenv()

yaml = YAML(typ="safe", pure=True)

# Load common.yaml as a base configuration
with open("configs/common.yaml", "r", encoding="utf-8") as yml_file:
    cfg = Box(yaml.load(yml_file))

env_config = os.getenv('ENVIRONMENT', 'PRODUCTION').upper()
config_file = cfg.config_file.local if env_config == "LOCAL" else cfg.config_file.prod

logger.info("Using configuration file: %s", config_file)

with open(f"configs/{config_file}", "r", encoding="utf-8") as yml_file:
    overrides = Box(yaml.load(yml_file))

cfg.merge_update(overrides)

# TODO: use secrets manager
cfg.discord.token = os.getenv('DISCORD_TOKEN')

logger.info("Configuration loaded: %s", cfg.to_dict())
