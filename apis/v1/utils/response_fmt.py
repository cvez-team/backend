from typing import Any
from fastapi.responses import JSONResponse


def jsonResponseFmt(data: Any, msg: str = "Success", code: int = 200, **kwargs):
    return JSONResponse({
        "msg": msg,
        "data": data
    }, code, **kwargs)
