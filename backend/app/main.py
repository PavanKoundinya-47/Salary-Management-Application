from contextlib import asynccontextmanager
from decimal import Decimal
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from .config import settings
from .database import Base, engine, get_db
from .models import Employee
from .schemas import EmployeeCreate, EmployeeOut, EmployeeUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Incubyte Salary Management API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "salary-management"}

@app.get("/api/employees", response_model=dict)
def list_employees(q: str | None = None, country: str | None = None, department: str | None = None, status: str | None = None, page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100), db: Session = Depends(get_db)):
    stmt = select(Employee)
    count_stmt = select(func.count(Employee.id))
    filters = []
    if q:
        term = f"%{q.strip()}%"
        filters.append(or_(Employee.first_name.ilike(term), Employee.last_name.ilike(term), Employee.email.ilike(term), Employee.employee_code.ilike(term), Employee.job_title.ilike(term)))
    if country: filters.append(Employee.country == country)
    if department: filters.append(Employee.department == department)
    if status: filters.append(Employee.employment_status == status)
    for f in filters: stmt = stmt.where(f); count_stmt = count_stmt.where(f)
    total = db.scalar(count_stmt) or 0
    rows = db.scalars(stmt.order_by(Employee.last_name, Employee.first_name).offset((page-1)*page_size).limit(page_size)).all()
    return {"items": [EmployeeOut.model_validate(x).model_dump(mode="json") for x in rows], "total": total, "page": page, "page_size": page_size, "pages": (total + page_size - 1)//page_size}

@app.post("/api/employees", response_model=EmployeeOut, status_code=201)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    if db.scalar(select(Employee.id).where(or_(Employee.employee_code == payload.employee_code, Employee.email == payload.email))):
        raise HTTPException(409, "Employee code or email already exists")
    employee = Employee(**payload.model_dump())
    db.add(employee)
    try: db.commit()
    except Exception:
        db.rollback(); raise HTTPException(409, "Employee code or email already exists")
    db.refresh(employee)
    return employee

@app.patch("/api/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.get(Employee, employee_id)
    if not employee: raise HTTPException(404, "Employee not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is not None: setattr(employee, key, value)
    db.commit(); db.refresh(employee)
    return employee

@app.get("/api/analytics")
def analytics(db: Session = Depends(get_db)):
    total = db.scalar(select(func.count(Employee.id))) or 0
    active = db.scalar(select(func.count(Employee.id)).where(Employee.employment_status == "Active")) or 0
    countries = db.scalar(select(func.count(func.distinct(Employee.country)))) or 0
    departments = db.scalar(select(func.count(func.distinct(Employee.department)))) or 0
    by_currency = db.execute(select(Employee.currency, func.count(Employee.id), func.avg(Employee.annual_salary), func.min(Employee.annual_salary), func.max(Employee.annual_salary)).group_by(Employee.currency).order_by(Employee.currency)).all()
    by_country = db.execute(select(Employee.country, Employee.currency, func.count(Employee.id), func.avg(Employee.annual_salary)).group_by(Employee.country, Employee.currency).order_by(func.count(Employee.id).desc()).limit(8)).all()
    by_department = db.execute(select(Employee.department, func.count(Employee.id)).group_by(Employee.department).order_by(func.count(Employee.id).desc())).all()
    return {"total_employees": total, "active_employees": active, "countries": countries, "departments": departments,
            "salary_by_currency": [{"currency": c, "employee_count": n, "average_salary": round(float(avg or 0),2), "min_salary": float(mn or 0), "max_salary": float(mx or 0)} for c,n,avg,mn,mx in by_currency],
            "salary_by_country": [{"country": c, "currency": cur, "employee_count": n, "average_salary": round(float(avg or 0),2)} for c,cur,n,avg in by_country],
            "employees_by_department": [{"department": d, "count": n} for d,n in by_department]}

@app.get("/api/filters")
def filters(db: Session = Depends(get_db)):
    return {"countries": list(db.scalars(select(Employee.country).distinct().order_by(Employee.country))), "departments": list(db.scalars(select(Employee.department).distinct().order_by(Employee.department))), "statuses": ["Active", "On leave", "Terminated"]}
