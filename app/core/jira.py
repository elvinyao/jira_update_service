import asyncio
from jira import JIRA
from app.config import load_config
from app.utils.logger import setup_logger
from app.models.schemas import JiraUpdateResult
from typing import List, Dict

logger = setup_logger(__name__)
config = load_config()


class JiraClient:
    def __init__(self):
        self.client = JIRA(
            server=config.jira_url,
            basic_auth=(config.bot_username, config.bot_password)
        )

    async def update_issues(self, filter_url: str, updates: Dict[str, str]) -> List[JiraUpdateResult]:
        try:
            issues = self.client.search_issues(filter_url)
            results = []
            for issue in issues:
                try:
                    fields_to_update = {}
                    for field, value in updates.items():
                        fields_to_update[field] = value

                    issue.update(fields=fields_to_update)
                    results.append(JiraUpdateResult(
                        success=True,
                        jira_key=issue.key,
                        message="Successfully updated",
                        updated_fields=fields_to_update
                    ))
                except Exception as e:
                    results.append(JiraUpdateResult(
                        success=False,
                        jira_key=issue.key,
                        message=f"Failed to update: {str(e)}",
                        updated_fields={}
                    ))
            return results
        except Exception as e:
            logger.error(f"Error updating Jira issues: {str(e)}")
            raise