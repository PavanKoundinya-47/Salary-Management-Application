"""Generate 10,000 deterministic demo employees; safe to rerun (upserts by employee_code)."""
import random
from sqlalchemy import select
from app.database import Base, SessionLocal, engine
from app.models import Employee

FIRST = ["Aarav", "Aditi", "Alex", "Amara", "Ananya", "Arjun", "Ava", "Daniel", "Fatima", "Ishaan", "Jia", "Liam", "Maya", "Noah", "Olivia", "Priya", "Ravi", "Sofia", "Theo", "Zara"]
LAST = ["Adams", "Brown", "Chen", "Das", "Garcia", "Gupta", "Iyer", "Johnson", "Khan", "Kim", "Lee", "Martin", "Patel", "Rao", "Sharma", "Singh", "Taylor", "Thomas", "Williams", "Wilson"]
ORG = [("India", "INR", 900000, 3200000), ("United States", "USD", 70000, 180000), ("United Kingdom", "GBP", 45000, 110000), ("Germany", "EUR", 48000, 115000), ("Singapore", "SGD", 65000, 150000), ("Australia", "AUD", 70000, 160000)]
DEPTS = {"Engineering": ["Software Engineer", "Senior Software Engineer", "Engineering Manager", "QA Engineer"], "Product": ["Product Manager", "Product Analyst", "UX Designer"], "People": ["HR Business Partner", "Recruiter", "People Operations Specialist"], "Finance": ["Financial Analyst", "Accountant", "Finance Manager"], "Sales": ["Account Executive", "Sales Manager", "Solutions Consultant"], "Operations": ["Operations Analyst", "Program Manager", "Support Specialist"]}

def main():
    Base.metadata.create_all(bind=engine)
    rng = random.Random(20261019)
    db = SessionLocal()
    try:
        existing = set(db.scalars(select(Employee.employee_code)))
        batch = []
        for i in range(1, 10001):
            code = f"EMP-{i:05d}"
            if code in existing: continue
            country, currency, low, high = ORG[(i * 7 + i // 13) % len(ORG)]
            dept = list(DEPTS)[(i * 3 + i // 17) % len(DEPTS)]
            first = FIRST[(i * 11) % len(FIRST)]; last = LAST[(i * 7) % len(LAST)]
            batch.append(Employee(employee_code=code, first_name=first, last_name=last, email=f"{code.lower()}@example.com", department=dept, job_title=DEPTS[dept][i % len(DEPTS[dept])], country=country, currency=currency, annual_salary=round(rng.uniform(low, high), 2), employment_status="Active" if i % 23 else ("On leave" if i % 46 == 0 else "Terminated")))
            if len(batch) == 1000: db.add_all(batch); db.commit(); batch = []
        if batch: db.add_all(batch); db.commit()
        print(f"Seed complete. Employees in database: {db.query(Employee).count()}")
    finally: db.close()

if __name__ == "__main__": main()
