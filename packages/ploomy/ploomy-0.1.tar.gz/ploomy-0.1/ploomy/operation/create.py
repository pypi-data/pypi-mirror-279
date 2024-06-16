from pydantic import BaseModel, field_validator

from .operation import Operation


class CreateOperation(BaseModel, Operation):
    filter_name: str
    capacity: int
    prob: float

    @field_validator("capacity")
    def check_capacity(cls, value):
        if value <= 10_000:
            raise ValueError("Capacity must be greater than 10,000")
        return value

    @field_validator("prob")
    def check_prob(cls, value):
        if value < 0 or value > 0.1:
            raise ValueError("Prob must be between (0, 0.1)")
        return value

    def compile(self):
        return f"create {self.filter_name} capacity={self.capacity} prob={self.prob}"


class CreateResult(BaseModel):
    status: str
    extra: str
