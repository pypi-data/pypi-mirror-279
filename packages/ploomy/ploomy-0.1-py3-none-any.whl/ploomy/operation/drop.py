from pydantic import BaseModel, field_validator

from .operation import Operation


class DropOperation(BaseModel, Operation):
    filter_name: str

    def compile(self):
        return f"drop {self.filter_name}"


class DropResult(BaseModel):
    status: str
    extra: str
