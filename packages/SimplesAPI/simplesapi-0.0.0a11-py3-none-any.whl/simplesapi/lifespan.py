from contextlib import asynccontextmanager
import logging
from urllib.parse import urlparse

import redis.asyncio as redis
from databases import Database

from simplesapi.types import Cache


logger = logging.getLogger("SimplesAPI")


@asynccontextmanager
async def lifespan(app):
    app.database = None
    app.cache = None
    await configure_database(app=app)
    await configure_cache(app=app)
    yield
    await close_database(app=app)
    await close_cache(app=app)


async def configure_database(app) -> None:
    if app.simples.database_url:
        database_info = extract_db_info(app.simples.database_url)
        logger.info(
            f"Configuring database | Host: {database_info['host']} | Database: {database_info['database']}"
        )
        app.database = Database(app.simples.database_url)
        await app.database.connect()
        await database_health_check(app)

async def database_health_check(app):
    try:
        await app.database.fetch_val("SELECT 1")
        logger.info("Database connection successful 🟩")
    except Exception as e:
        logger.error("Failed to connect to database 🟥")
        app.database = None
        raise e


async def configure_cache(app) -> None:
    if app.simples.cache_url:
        redis_info = extract_db_info(app.simples.cache_url)
        logger.info(
            f"Configuring cache | Host: {redis_info['host']}"
        )
        redis_conn = redis.ConnectionPool.from_url(
            app.simples.cache_url, encoding="utf-8", decode_responses=True
        )
        app.cache = Cache(redis.Redis(connection_pool=redis_conn))
        await cache_health_check(app)
    else:
        app.cache = None

async def cache_health_check(app):
    try:
        await app.cache.redis.ping()
        logger.info("Cache connection successful 🟩")
    except redis.exceptions.ConnectionError:
        logger.error("Failed to connect to cache 🟥")
        app.cache = None


def extract_db_info(db_url: str) -> dict:
    parsed_url = urlparse(db_url)
    host = parsed_url.hostname
    db_name = parsed_url.path.lstrip("/")  # Remove leading slash

    return {"host": host, "database": db_name}


async def close_database(app) -> Database:
    if app.database:
        database_info = extract_db_info(app.simples.database_url)
        logger.info(
            f"Closing database | Host: {database_info['host']} | Database: {database_info['database']}"
        )
        await app.database.disconnect()


async def close_cache(app) -> Database:
    if app.cache:
        cache_info = extract_db_info(app.simples.cache_url)
        logger.info(
            f"Closing database | Host: {cache_info['host']} | Database: {cache_info['database']}"
        )
        await app.cache.close()


