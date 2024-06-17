import importlib
import logging
import os
from fastapi import FastAPI
from simplesapi.request import SRequest


logger = logging.getLogger("SimplesAPI")


def _import_handler(module_path, handler_name="handler"):
    spec = importlib.util.spec_from_file_location("routes", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, handler_name)


def _create_route_from_file(app: FastAPI, file_path: str, base_path: str) -> None:
    parts = file_path.split(os.sep)
    method_file_result = parts[-1].split(".")[0].split("__")

    last_route = method_file_result[0] if len(method_file_result) > 1 else ""
    last_route = last_route.replace("[", "{").replace("]", "}")
    method = method_file_result[-1].upper()

    route = os.sep.join(parts[:-1])
    route = route.replace(base_path, "", 1)
    route = route.replace("[", "{").replace("]", "}")
    route = (
        "/" + route.strip(os.sep).replace(os.sep, "/") + "/" if len(route) > 0 else "/"
    )

    if last_route:
        route += last_route

    handler = _import_handler(file_path)
    s_handler = SRequest(route=route, handler=handler, method=method)
    available_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    if method in available_methods:
        app.add_api_route(route, s_handler.request)
        logger.info(f"Added route {method.upper()} {route}")


def register_routes(app, base_path: str):
    base_path = base_path.replace("/", os.sep)
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                _create_route_from_file(app, file_path, base_path)
