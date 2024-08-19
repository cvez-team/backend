from typing import Callable
import time
import logging
from colorama import Fore, Style


logger = logging.getLogger("uvicorn.info")


def prefix_color_map(prefix: str):
    _mapped_color = {
        "DATABASE": Fore.YELLOW,
        "VECTOR_DATABASE": Fore.RED,
        "LLM": Fore.CYAN,
        "CACHE": Fore.BLUE,
    }.get(prefix, Fore.WHITE)
    return f"[{_mapped_color + prefix + Style.RESET_ALL}]"


def logger_decorator(prefix: str = "FEATURE"):
    """
    Decorator for logging the execution time of a function
    """
    def _wrapper(func: Callable):
        def _inner(self, *args, **kwargs):
            _s = time.perf_counter()
            result = func(self, *args, **kwargs)
            _e = time.perf_counter() - _s
            logger.info(
                f"{prefix_color_map(prefix)} ({func.__name__}) executed [{_e:.2f}s]")
            return result
        return _inner
    return _wrapper


def log_database(msg: str):
    prefix = f"{Fore.YELLOW}DATABASE{Style.RESET_ALL}:"
    print(prefix + " ", end="")
    print(msg)


def log_qdrant(msg: str):
    prefix = f"{Fore.RED}QDRANT{Style.RESET_ALL}:"
    print(prefix + " "*3, end="")
    print(msg)


def log_llm(msg: str):
    prefix = f"{Fore.CYAN}LLM{Style.RESET_ALL}:"
    print(prefix + " "*6, end="")
    print(msg)


def log_cache(msg: str):
    prefix = f"{Fore.BLUE}CACHE{Style.RESET_ALL}:"
    print(prefix + " "*4, end="")
    print(msg)
