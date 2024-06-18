from typing import Callable, Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel

import inspect

# 라우터를 모듈별로 저장할 딕셔너리
module_routers: Dict[str, APIRouter] = {}

def get_router_for_module(module_name: str) -> APIRouter:
    if module_name not in module_routers:
        module_routers[module_name] = APIRouter()
    return module_routers[module_name]

def data_conv(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs).arguments

        for name, param in sig.parameters.items():
            param_class = param.annotation
            if name in bound_args:
                if isinstance(bound_args[name], dict) and issubclass(param_class, BaseModel):
                    bound_args[name] = param_class(**bound_args[name])
                else:
                    bound_args[name] = bound_args[name]

        return func(*bound_args.values())

    return wrapper

def auto_schema(func: Callable) -> Callable:
    func_name = func.__name__
    module = inspect.getmodule(func)
    if module is None:
        raise ValueError("Module not found for the given function")
    module_name = module.__name__
    path = f"/{module_name.replace('.', '/')}/{func_name}"

    router = get_router_for_module(module_name + func_name)
    router.add_api_route(path, func, methods=["POST"])
    return data_conv(func)
