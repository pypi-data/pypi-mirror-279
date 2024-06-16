from pydantic import BaseModel
from typing import Dict, Any

from .operation import Operation


class InfoOperation(BaseModel, Operation):
    filter_name: str

    def compile(self):
        return f"info {self.filter_name}"


class InfoResult(BaseModel):
    result: Dict[str, Any]
