from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ConfluenceTableRow(BaseModel):
    description: str
    creator: str
    jira_filter_url: str
    update_config_url: str
    cron_expression: str
    mattermost_channel: str
    bot_token_page_url: Optional[str]
    bot_message: str

class ConfluenceConfig(BaseModel):
    timestamp: datetime
    rows: List[ConfluenceTableRow]

class JiraUpdateResult(BaseModel):
    success: bool
    jira_key: str
    message: str
    updated_fields: Dict[str, str]