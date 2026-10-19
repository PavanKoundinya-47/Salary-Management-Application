from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

class EmployeeBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: str = Field(min_length=3, max_length=160)
    department: str = Field(min_length=1, max_length=80)
    job_title: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=1, max_length=80)
    currency: str = Field(min_length=3, max_length=3)
    annual_salary: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    employment_status: str = "Active"

    @field_validator("currency")
    @classmethod
    def currency_uppercase(cls, v: str) -> str:
        return v.upper()

    @field_validator("employment_status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        if v not in {"Active", "On leave", "Terminated"}:
            raise ValueError("Status must be Active, On leave, or Terminated")
        return v

class EmployeeCreate(EmployeeBase):
    employee_code: str = Field(min_length=1, max_length=20)

class EmployeeUpdate(BaseModel):
    annual_salary: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    department: str | None = Field(default=None, min_length=1, max_length=80)
    job_title: str | None = Field(default=None, min_length=1, max_length=100)
    employment_status: str | None = None

    @field_validator("employment_status")
    @classmethod
    def valid_status(cls, v):
        if v is not None and v not in {"Active", "On leave", "Terminated"}:
            raise ValueError("Status must be Active, On leave, or Terminated")
        return v

class EmployeeOut(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_code: str
    updated_at: datetime
