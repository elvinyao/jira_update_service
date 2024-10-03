import yaml
from pydantic import BaseSettings
from typing import List, Dict, Optional

class Settings(BaseSettings):
    confluence_urls: List[str]
    bot_username: str
    bot_password: str
    mattermost_url: str
    common_bot_token: str
    error_notice_channel_url: str
    sleep_sec: int = 300
    log_path: str = "./logs"
    thread_limit: int = 5
    log_max_days: int = 30
    log_max_size: int = 2 * 1024 * 1024  # 2MB

    class Config:
        env_file = ".env"

def load_config() -> Settings:
    with open("config.yaml") as f:
        config_data = yaml.safe_load(f)
    return Settings(**config_data)