from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.employee_service import EmployeeService

class EmployeeController:

    @staticmethod
    def create(emp_data: EmployeeCreate, db: Session):
        return EmployeeService.create_employee(db, emp_data)

    @staticmethod
    def get_all(
        db: Session, 
        search: Optional[str], 
        department: Optional[str], 
        min_salary: Optional[float], 
        max_salary: Optional[float], 
        page: int, 
        limit: int
    ):
        return EmployeeService.get_employees(db, search, department, min_salary, max_salary, page, limit)

    @staticmethod
    def get_by_id(emp_id: int, db: Session):
        return EmployeeService.get_employee_by_id(db, emp_id)

    @staticmethod
    def update(emp_id: int, emp_data: EmployeeCreate, db: Session):
        return EmployeeService.update_employee(db, emp_id, emp_data)

    @staticmethod
    def patch(emp_id: int, emp_data: EmployeeUpdate, db: Session):
        return EmployeeService.patch_employee(db, emp_id, emp_data)

    @staticmethod
    def delete(emp_id: int, db: Session):
        return EmployeeService.delete_employee(db, emp_id)