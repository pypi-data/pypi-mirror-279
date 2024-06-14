from typing import Callable, Any
import inspect
from pydantic import BaseModel


def auto_convert(func: Callable) -> Callable:
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
