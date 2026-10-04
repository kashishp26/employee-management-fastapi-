from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.department import DepartmentCreate, DepartmentResponse
from app.schemas.employee import EmployeeResponse
from app.controllers.department_controller import DepartmentController
from app.dependencies.auth_deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    dept_data: DepartmentCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return DepartmentController.create(dept_data, db)

@router.get("/", response_model=List[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return DepartmentController.get_all(db)

@router.get("/{department_id}/employees", response_model=List[EmployeeResponse])
def get_department_employees(
    department_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return DepartmentController.get_employees(department_id, db)