# app/services/jira_service.py
import asyncio
from app.core.jira import JiraClient
from app.utils.logger import setup_logger
from app.config import load_config
from typing import List
from app.models.schemas import JiraUpdateResult

logger = setup_logger(__name__)
config = load_config()

class JiraService:
    def __init__(self):
        self.client = JiraClient()
        self._semaphore = asyncio.Semaphore(config.thread_limit)

    async def start(self):
        pass

    async def stop(self):
        pass

    async def update_issues(self, filter_url: str, updates: dict) -> List[JiraUpdateResult]:
        async with self._semaphore:
            return await self.client.update_issues(filter_url, updates)