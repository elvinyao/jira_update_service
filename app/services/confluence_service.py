# app/services/confluence_service.py
import asyncio
from app.core.confluence import ConfluenceClient
from app.utils.logger import setup_logger
from app.config import load_config
from typing import Dict, List
from app.models.schemas import ConfluenceConfig

logger = setup_logger(__name__)
config = load_config()

class ConfluenceService:
    def __init__(self):
        self.client = ConfluenceClient()
        self.configs: Dict[str, ConfluenceConfig] = {}

    async def start(self):
        await self.refresh_configs()

    async def stop(self):
        pass

    async def refresh_configs(self):
        for url in config.confluence_urls:
            try:
                page_config = await self.client.get_table_config(url)
                self.configs[url] = page_config
            except Exception as e:
                logger.error(f"Error refreshing config for {url}: {str(e)}")

    async def get_all_configs(self) -> List[ConfluenceConfig]:
        return list(self.configs.values())