from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.employee import Employee
from app.schemas.department import DepartmentCreate
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class DepartmentService:

    @staticmethod
    def create_department(db: Session, dept_data: DepartmentCreate):
        existing = db.query(Department).filter(Department.name == dept_data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department already exists"
            )
        new_dept = Department(name=dept_data.name)
        db.add(new_dept)
        db.commit()
        db.refresh(new_dept)
        return new_dept

    @staticmethod
    def get_all_departments(db: Session):
        return db.query(Department).all()

    @staticmethod
    def get_department_employees(db: Session, department_id: int):
        dept = db.query(Department).filter(Department.id == department_id).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        return dept.employees


class EmployeeService:

    @staticmethod
    def create_employee(db: Session, emp_data: EmployeeCreate):
        dept = db.query(Department).filter(Department.id == emp_data.department_id).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid department_id. Department does not exist."
            )
        
        existing = db.query(Employee).filter(Employee.email == emp_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee with this email already exists."
            )

        new_emp = Employee(**emp_data.model_dump())
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        return new_emp

    @staticmethod
    def get_employees(
        db: Session, 
        search: Optional[str] = None, 
        department: Optional[str] = None, 
        min_salary: Optional[float] = None, 
        max_salary: Optional[float] = None, 
        page: int = 1, 
        limit: int = 10
    ):
        query = db.query(Employee)

        if search:
            query = query.filter(Employee.name.ilike(f"%{search}%"))
        if department:
            query = query.join(Department).filter(Department.name.ilike(f"%{department}%"))
        if min_salary is not None:
            query = query.filter(Employee.salary >= min_salary)
        if max_salary is not None:
            query = query.filter(Employee.salary <= max_salary)

        offset = (page - 1) * limit
        return query.offset(offset).limit(limit).all()

    @staticmethod
    def get_employee_by_id(db: Session, emp_id: int):
        emp = db.query(Employee).filter(Employee.id == emp_id).first()
        if not emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return emp

    @staticmethod
    def update_employee(db: Session, emp_id: int, emp_data: EmployeeCreate):
        emp = EmployeeService.get_employee_by_id(db, emp_id)
        
        dept = db.query(Department).filter(Department.id == emp_data.department_id).first()
        if not dept:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid department_id")

        for key, value in emp_data.model_dump().items():
            setattr(emp, key, value)

        db.commit()
        db.refresh(emp)
        return emp

    @staticmethod
    def patch_employee(db: Session, emp_id: int, emp_data: EmployeeUpdate):
        emp = EmployeeService.get_employee_by_id(db, emp_id)
        
        update_data = emp_data.model_dump(exclude_unset=True)
        if "department_id" in update_data:
            dept = db.query(Department).filter(Department.id == update_data["department_id"]).first()
            if not dept:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid department_id")

        for key, value in update_data.items():
            setattr(emp, key, value)

        db.commit()
        db.refresh(emp)
        return emp

    @staticmethod
    def delete_employee(db: Session, emp_id: int):
        emp = EmployeeService.get_employee_by_id(db, emp_id)
        db.delete(emp)
        db.commit()
        return {"message": f"Employee {emp_id} deleted successfully"}