from pydantic import BaseModel

from .operation import Operation


class ListOperation(BaseModel, Operation):
    filter_name: str

    def compile(self):
        return f"list {self.filter_name}"


class ListResult(BaseModel):
    filter_name: str
    capacity: int
    prob: float
    size: int
