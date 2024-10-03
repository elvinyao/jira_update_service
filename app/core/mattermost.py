import aiohttp
from app.config import load_config
from app.utils.logger import setup_logger
from app.models.schemas import JiraUpdateResult
from typing import List

logger = setup_logger(__name__)
config = load_config()


class MattermostClient:
    def __init__(self):
        self.base_url = config.mattermost_url
        self.token = config.common_bot_token

    async def send_notification(self, channel_url: str, message: str):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(channel_url, json={"text": message}, headers=headers) as response:
                    if response.status != 200:
                        logger.error(f"Failed to send Mattermost notification: {await response.text()}")
                    return response.status == 200
            except Exception as e:
                logger.error(f"Error sending Mattermost notification: {str(e)}")
                return False

    async def send_update_results(self, channel_url: str, results: List[JiraUpdateResult]):
        message = "Jira Update Results:\n"
        for result in results:
            status = "✅" if result.success else "❌"
            message += f"{status} {result.jira_key}: {result.message}\n"

        return await self.send_notification(channel_url, message)