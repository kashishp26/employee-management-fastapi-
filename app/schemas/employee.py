from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.schemas.department import DepartmentResponse

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    salary: float = Field(gt=0, description="Salary must be greater than 0")
    department_id: int

class EmployeeCreate(EmployeeBase):
    pass

# For PUT (Full Update) / PATCH (Partial Update)
class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    salary: Optional[float] = Field(None, gt=0)
    department_id: Optional[int] = None

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    salary: float
    department_id: int
    department: Optional[DepartmentResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True