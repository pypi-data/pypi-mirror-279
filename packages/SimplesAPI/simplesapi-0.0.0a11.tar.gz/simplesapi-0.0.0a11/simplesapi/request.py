from typing import Any, Callable
from starlette.requests import HTTPConnection
from starlette.exceptions import HTTPException
import inspect

from simplesapi.types import Cache, Database


class SRequest:
    def __init__(self, route: str, handler: Callable, method: str, simples_extra: Any = None):
        self.handler = handler
        self.method = method
        self.route = route
        self.simples_extra = simples_extra
        self.injected_params = None
        self.handler_params = inspect.signature(self.handler).parameters.values()
        self.handle_param_names = [param.name for param in self.handler_params]

    def extract_route_params(self):
        """Extract route parameters from the route string"""
        parts = self.route.split("/")
        return [
            part[1:-1] for part in parts if part.startswith("{") and part.endswith("}")
        ]

    def inject_params(self, request: HTTPConnection, handler_params: list):
        if not self.injected_params:
            self.injected_params = {}
            if hasattr(request.app, "database"):
                [
                    self.injected_params.update(
                        {handle_param.name: request.app.database}
                    )
                    for handle_param in handler_params
                    if handle_param.annotation is Database
                ]
            if hasattr(request.app, "cache"):
                [
                    self.injected_params.update({handle_param.name: request.app.cache})
                    for handle_param in handler_params
                    if handle_param.annotation is Cache
                ]

    async def request(self, request: HTTPConnection):
        route_params = self.extract_route_params()
        request_params = request.path_params
        query_params = request.query_params

        self.inject_params(request, self.handler_params)

        path_params = {
            param: request.path_params[param]
            for param in route_params
            if param in request_params and param in self.handle_param_names
        }
        query_params = {
            param: request.query_params[param]
            for param in query_params
            if param not in request_params and param in self.handle_param_names
        }
        extra_params = {"_simples_extra": self.simples_extra} if "_simples_extra" in self.handle_param_names else {}
        
        missing_params = [
            param
            for param in self.handle_param_names
            if param not in path_params.keys()
            and param not in query_params.keys()
            and param not in self.injected_params.keys()
            and param not in ["_simples_extra"]
        ]
        
        if missing_params:
            raise HTTPException(
                status_code=400, detail=f"Missing fields: {";".join(missing_params)}"
            )
        return await self.handler(**path_params, **self.injected_params, **query_params, **extra_params)
