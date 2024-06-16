from pydantic import BaseModel
from typing import Dict, Any

from .operation import Operation


class SetOperation(BaseModel, Operation):
    filter_name: str
    value: str

    def compile(self):
        return f"set {self.filter_name} {self.value}"


class SetResult(BaseModel):
    status: str
