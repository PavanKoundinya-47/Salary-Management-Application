from datetime import datetime, timezone
from sqlalchemy import String, Integer, Numeric, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        Index("ix_employees_name", "first_name", "last_name"),
        Index("ix_employees_department_country", "department", "country"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    department: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    job_title: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    annual_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    employment_status: Mapped[str] = mapped_column(String(20), default="Active", index=True, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
