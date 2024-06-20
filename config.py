import os
from box import Box
from ruamel.yaml import YAML
from dotenv import load_dotenv
from common.logger import logger


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        load_dotenv()
        yaml = YAML(typ="safe", pure=True)

        # Load common.yaml as a base configuration
        with open("configs/common.yaml", "r", encoding="utf-8") as yml_file:
            self.data = Box(yaml.load(yml_file))

        env_config = os.getenv("ENVIRONMENT", "PRODUCTION").upper()
        config_file = (
            self.data.config_file.local
            if env_config == "LOCAL"
            else self.data.config_file.prod
        )

        logger.info("Using configuration file: %s", config_file)

        with open(f"configs/{config_file}", "r", encoding="utf-8") as yml_file:
            overrides = Box(yaml.load(yml_file))

        self.data.merge_update(overrides)

        # TODO: use secrets manager
        self.data.discord.token = os.getenv("DISCORD_TOKEN")

        logger.info("Configuration loaded: %s", self.data.to_dict())

    def __getattr__(self, name):
        return getattr(self.data, name)

    def __setattr__(self, name, value):
        if name in {"data", "_instance"}:
            super().__setattr__(name, value)
        else:
            setattr(self.data, name, value)

    def exists(self, name):
        return hasattr(self.data, name)


# Singleton instance
cfg = Config()
