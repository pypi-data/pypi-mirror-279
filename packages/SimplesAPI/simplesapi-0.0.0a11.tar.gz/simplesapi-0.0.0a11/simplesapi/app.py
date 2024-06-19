from typing import Any, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

from simplesapi import lifespan, settings
from simplesapi.auto_routing import register_routes


from simplesapi.internal_logger import simplesapi_internal_logger

class SimplesConfig(BaseModel):
    verbose: Optional[bool] = Field(default=False)
    base_path: Optional[str] = Field(default="/")
    routes_path: Optional[str] = Field(default="routes")
    cache_url: Optional[str] = Field(default=settings.SIMPLESAPI_CACHE_URL)
    cache_ssl: Optional[bool] = Field(default=settings.SIMPLESAPI_CACHE_SSL)
    database_url: Optional[str] = Field(
        default=settings.SIMPLES_DABASE_URL
    )
    database_metadata: Optional[Any] = Field(
        default=None
    )


class SimplesAPI(FastAPI):
    def __init__(
        self, routes_path=None, cache_url=None, cache_ssl=None, database_url=None, *args, **kwargs
    ):
        simplesapi_internal_logger()
        self.simples = SimplesConfig(
            routes_path=routes_path, cache_url=cache_url, cache_ssl=cache_ssl, database_url=database_url, **kwargs
        )
        super().__init__(lifespan=lifespan.lifespan, *args, **kwargs)
        if self.simples.routes_path:
            register_routes(self, self.simples.routes_path)
