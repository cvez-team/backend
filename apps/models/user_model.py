from plugins.typing import LLMFmt


class UserModel:
    def __init__(self, uid: str, fmt: LLMFmt):
        self.id = uid
        self.fmt = fmt
