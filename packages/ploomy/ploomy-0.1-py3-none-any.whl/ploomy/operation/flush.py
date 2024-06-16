from pydantic import BaseModel
from typing import Optional

from .operation import Operation


class FlushOperation(BaseModel, Operation):
    filter_name: Optional[str] = ""

    def compile(self):
        return f"flush {self.filter_name}".strip()


class FlushResult(BaseModel):
    status: str
    extra: str
