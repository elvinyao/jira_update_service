# app/services/notification_service.py
from app.core.mattermost import MattermostClient
from app.utils.logger import setup_logger
from app.models.schemas import JiraUpdateResult
from typing import List

logger = setup_logger(__name__)

class NotificationService:
    def __init__(self):
        self.client = MattermostClient()

    async def send_update_results(self, channel_url: str, results: List[JiraUpdateResult]):
        return await self.client.send_update_results(channel_url, results)