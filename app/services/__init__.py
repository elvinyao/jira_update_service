"""
Services Package

This package contains the core services for the Jira Auto Update application.
It provides high-level interfaces for interacting with Confluence, Jira,
and Mattermost, as well as orchestrating the update process.
"""

from app.services.confluence_service import ConfluenceService
from app.services.jira_service import JiraService
from app.services.notification_service import NotificationService
from app.utils.logger import setup_logger
from typing import Dict, Any
import asyncio
from app.config import load_config

logger = setup_logger(__name__)

__all__ = [
    "ConfluenceService",
    "JiraService",
    "NotificationService",
    "ServiceManager"
]


class ServiceManager:
    """
    Manages the lifecycle and coordination of all services.
    Provides a central point for starting, stopping, and accessing services.
    """

    def __init__(self):
        self.config = load_config()
        self.confluence_service = ConfluenceService()
        self.jira_service = JiraService()
        self.notification_service = NotificationService()
        self._is_running = False

    async def start(self) -> None:
        """Start all services."""
        if self._is_running:
            logger.warning("Services are already running")
            return

        logger.info("Starting all services")
        try:
            await asyncio.gather(
                self.confluence_service.start(),
                self.jira_service.start(),
            )
            self._is_running = True
            logger.info("All services started successfully")
        except Exception as e:
            logger.error(f"Failed to start services: {str(e)}")
            await self.stop()
            raise

    async def stop(self) -> None:
        """Stop all services gracefully."""
        if not self._is_running:
            logger.warning("Services are not running")
            return

        logger.info("Stopping all services")
        try:
            await asyncio.gather(
                self.confluence_service.stop(),
                self.jira_service.stop(),
            )
        except Exception as e:
            logger.error(f"Error during service shutdown: {str(e)}")
        finally:
            self._is_running = False
            logger.info("All services stopped")

    @property
    def is_running(self) -> bool:
        """Return the running status of services."""
        return self._is_running

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on all services."""
        health_status = {
            "overall_status": "healthy",
            "services": {
                "confluence": "healthy",
                "jira": "healthy",
                "notification": "healthy"
            }
        }

        try:
            # Add specific health checks for each service
            # These methods need to be implemented in each service class
            confluence_health = await self.confluence_service.health_check()
            jira_health = await self.jira_service.health_check()

            if not confluence_health:
                health_status["services"]["confluence"] = "unhealthy"
                health_status["overall_status"] = "degraded"

            if not jira_health:
                health_status["services"]["jira"] = "unhealthy"
                health_status["overall_status"] = "degraded"

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            health_status["overall_status"] = "unhealthy"
            health_status["error"] = str(e)

        return health_status


# Create a global service manager instance
service_manager = ServiceManager()


# Helper functions for easy access to services
def get_confluence_service() -> ConfluenceService:
    return service_manager.confluence_service


def get_jira_service() -> JiraService:
    return service_manager.jira_service


def get_notification_service() -> NotificationService:
    return service_manager.notification_service