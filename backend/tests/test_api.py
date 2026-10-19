import os
os.environ["DATABASE_URL"] = "sqlite:///./test_salary_management.db"
os.environ["CORS_ORIGINS"] = "http://localhost:5173"
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Employee

Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    db.add(Employee(employee_code="EMP-00001", first_name="Asha", last_name="Rao", email="asha@example.com", department="Engineering", job_title="Software Engineer", country="India", currency="INR", annual_salary=1200000, employment_status="Active"))
    db.commit()
client = TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "ok"

def test_list_and_search():
    response = client.get("/api/employees?q=Asha")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["employee_code"] == "EMP-00001"

def test_patch_salary():
    response = client.patch("/api/employees/1", json={"annual_salary": 1400000})
    assert response.status_code == 200
    assert float(response.json()["annual_salary"]) == 1400000

def test_analytics_never_aggregates_different_currencies():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_employees"] == 1
    assert data["salary_by_currency"][0]["currency"] == "INR"
