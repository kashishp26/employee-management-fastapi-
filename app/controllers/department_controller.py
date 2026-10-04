from sqlalchemy.orm import Session
from app.schemas.department import DepartmentCreate
from app.services.employee_service import DepartmentService

class DepartmentController:

    @staticmethod
    def create(dept_data: DepartmentCreate, db: Session):
        return DepartmentService.create_department(db, dept_data)

    @staticmethod
    def get_all(db: Session):
        return DepartmentService.get_all_departments(db)

    @staticmethod
    def get_employees(department_id: int, db: Session):
        return DepartmentService.get_department_employees(db, department_id)