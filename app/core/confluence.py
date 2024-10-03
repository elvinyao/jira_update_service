import asyncio
from atlassian import Confluence
from app.config import load_config
from app.utils.logger import setup_logger
from app.models.schemas import ConfluenceTableRow, ConfluenceConfig
from typing import List, Dict
import pandas as pd
from datetime import datetime

logger = setup_logger(__name__)
config = load_config()

class ConfluenceClient:
    def __init__(self):
        self.client = Confluence(
            url=config.confluence_urls[0],
            username=config.bot_username,
            password=config.bot_password
        )
        self._cache = {}
        self._cache_time = None

    async def get_table_config(self, page_id: str) -> ConfluenceConfig:
        if self._cache_time and (datetime.now() - self._cache_time).seconds < config.sleep_sec:
            return self._cache.get(page_id)

        try:
            page_content = self.client.get_page_by_id(page_id, expand='body.storage')
            # Parse HTML content to extract table data
            # This is a simplified version; you might need a more robust HTML parsing
            tables = pd.read_html(page_content['body']['storage']['value'])
            if not tables:
                raise ValueError(f"No tables found in Confluence page {page_id}")

            rows = []
            for _, row in tables[0].iterrows():
                row_data = ConfluenceTableRow(
                    description=row['Description'],
                    creator=row['Creator'],
                    jira_filter_url=row['JIRA Filter URL'],
                    update_config_url=row['Update Config URL'],
                    cron_expression=row['Cron Expression'],
                    mattermost_channel=row['Mattermost Channel'],
                    bot_token_page_url=row.get('Bot Token Page URL'),
                    bot_message=row['Bot Message']
                )
                rows.append(row_data)

            config = ConfluenceConfig(timestamp=datetime.now(), rows=rows)
            self._cache[page_id] = config
            self._cache_time = datetime.now()
            return config
        except Exception as e:
            logger.error(f"Error fetching Confluence page {page_id}: {str(e)}")
            raise

    async def update_excel_file(self, page_id: str, results: List[JiraUpdateResult]):
        # Implementation for updating Excel file in Confluence
        pass