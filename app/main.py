# app/main.py
import asyncio
import signal
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from app.config import load_config
from app.services.confluence_service import ConfluenceService
from app.services.jira_service import JiraService
from app.services.notification_service import NotificationService
from app.utils.logger import setup_logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

logger = setup_logger(__name__)
config = load_config()


class AppState:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.confluence_service = ConfluenceService()
        self.jira_service = JiraService()
        self.notification_service = NotificationService()

    async def start(self):
        await self.confluence_service.start()
        await self.jira_service.start()
        self.scheduler.start()

    async def stop(self):
        self.scheduler.shutdown()
        await self.confluence_service.stop()
        await self.jira_service.stop()


app_state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await app_state.start()

    def signal_handler():
        asyncio.create_task(shutdown())

    for sig in (signal.SIGTERM, signal.SIGINT):
        asyncio.get_event_loop().add_signal_handler(sig, signal_handler)

    try:
        yield
    finally:
        await app_state.stop()


app = FastAPI(lifespan=lifespan)


async def shutdown():
    logger.info("Shutting down gracefully...")
    await app_state.stop()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/api/confluence/config")
async def get_confluence_config():
    try:
        configs = await app_state.confluence_service.get_all_configs()
        return {"configs": configs}
    except Exception as e:
        logger.error(f"Error fetching Confluence configs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Jira Auto Update Service",
        version="1.0.0",
        description="A service for automatically updating Jira tickets based on Confluence configurations",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    logger.info("Application starting...")

    uvicorn.run(app, host="0.0.0.0", port=8000)
