"""
Jira Auto Update Service

This package provides automated Jira ticket updates based on Confluence configurations.
It includes functionality for reading Confluence tables, updating Jira tickets,
and sending notifications via Mattermost.
"""

from app.config import load_config
from app.core.confluence import ConfluenceClient
from app.core.jira import JiraClient
from app.core.mattermost import MattermostClient
from app.services.confluence_service import ConfluenceService
from app.services.jira_service import JiraService
from app.services.notification_service import NotificationService

# Version information
__version__ = "1.0.0"
__author__ = "Your Company Name"
__license__ = "Proprietary"

# Expose key components for easy access
__all__ = [
    "load_config",
    "ConfluenceClient",
    "JiraClient",
    "MattermostClient",
    "ConfluenceService",
    "JiraService",
    "NotificationService",
]

# Initialize logger
from app.utils.logger import setup_logger
logger = setup_logger(__name__)

def get_version():
    """Return the current version of the package."""
    return __version__

# Optional: Add any package-level initialization if needed
def initialize():
    """Initialize the package if any setup is required."""
    logger.info(f"Initializing Jira Auto Update Service v{__version__}")
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Failed to initialize: {str(e)}")
        raise

# Optional: Cleanup function if needed
def cleanup():
    """Cleanup function to be called when shutting down."""
    logger.info("Performing cleanup")
    # Add any necessary cleanup code here

# Initialization code that runs when the package is imported
try:
    config = initialize()
except Exception as e:
    logger.error(f"Package initialization failed: {str(e)}")
    raise