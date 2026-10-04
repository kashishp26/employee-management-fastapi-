from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.controllers.employee_controller import EmployeeController
from app.dependencies.auth_deps import get_current_user, require_admin
from app.models.user import User

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    emp_data: EmployeeCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return EmployeeController.create(emp_data, db)

@router.get("/", response_model=List[EmployeeResponse])
def get_employees(
    search: Optional[str] = Query(None, description="Search by name"),
    department: Optional[str] = Query(None, description="Filter by department name"),
    min_salary: Optional[float] = Query(None, description="Filter minimum salary"),
    max_salary: Optional[float] = Query(None, description="Filter maximum salary"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return EmployeeController.get_all(db, search, department, min_salary, max_salary, page, limit)

@router.get("/{id}", response_model=EmployeeResponse)
def get_employee_by_id(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return EmployeeController.get_by_id(id, db)

@router.put("/{id}", response_model=EmployeeResponse)
def update_employee(
    id: int, 
    emp_data: EmployeeCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return EmployeeController.update(id, emp_data, db)

@router.patch("/{id}", response_model=EmployeeResponse)
def patch_employee(
    id: int, 
    emp_data: EmployeeUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return EmployeeController.patch(id, emp_data, db)

@router.delete("/{id}")
def delete_employee(
    id: int, 
    db: Session = Depends(get_db), 
    admin_user: User = Depends(require_admin) # Strictly ADMIN role check
):
    return EmployeeController.delete(id, db)