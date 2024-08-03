import os
import toml
import dacite

from dataclasses import dataclass


@dataclass
class ConfigBot:
    token: str


@dataclass
class ConfigSettings:
    database_url: str


@dataclass
class Config:
    bot: ConfigBot
    settings: ConfigSettings


def parse_config() -> Config:
    config_file = "config.toml"
    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file} no such file")

    with open(config_file, "r", encoding="utf-8") as file:
        data = toml.load(file)

    return dacite.from_dict(data_class=Config, data=data)
