"""Single module for package wtforglib."""

import threading
from typing import Callable, Type, TypeVar

T = TypeVar("T")  # noqa: WPS111


def singleton(cls: Type[T]) -> Callable[..., T]:  # type: ignore [explicit-any]
    instances: dict[Type[T], T] = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs) -> T:  # noqa: WPS430
        if cls not in instances:
            # If no instance has been created yet, create one
            instances[cls] = cls(*args, **kwargs)
        # Return the single instance
        return instances[cls]

    return get_instance
