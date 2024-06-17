from pydantic import BaseModel
from typing import Optional
from aiohttp.abc import AbstractCookieJar


class CaseRespnseModel(BaseModel):
    output:Optional[dict] = None
    cookie_jar:Optional[AbstractCookieJar] = None

    class Config:
        arbitrary_types_allowed = True