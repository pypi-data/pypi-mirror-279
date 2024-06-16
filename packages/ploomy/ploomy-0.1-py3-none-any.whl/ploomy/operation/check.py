from pydantic import BaseModel
from typing import Dict, Any

from .operation import Operation


class CheckOperation(BaseModel, Operation):
    filter_name: str
    value: str

    def compile(self):
        return f"check {self.filter_name} {self.value}"


class CheckResult(BaseModel):
    status: str
