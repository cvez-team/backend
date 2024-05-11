from colorama import Fore, Style


def log_firebase(msg: str):
    prefix = f"{Fore.YELLOW}FIREBASE{Style.RESET_ALL}:"
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
