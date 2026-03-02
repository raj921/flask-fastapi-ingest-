import os
import requests
from datetime import datetime
from models.customer import Customer

MOCK_URL = os.getenv("MOCK_URL", "http://mock-server:5000")

def fetch_all():
    all_data = []
    page = 1
    limit = 20
    while True:
        r = requests.get(f"{MOCK_URL}/api/customers", params={"page": page, "limit": limit})
        r.raise_for_status()
        data = r.json()
        all_data.extend(data["data"])
        if len(data["data"]) < limit:
            break
        page += 1
    return all_data

def upsert_batch(db, rows):
    count = 0
    for row in rows:
        dob = None
        if row.get("date_of_birth"):
            dob = datetime.fromisoformat(row["date_of_birth"].replace("Z", "+00:00")).date()
        existing = db.query(Customer).filter(Customer.customer_id == row["customer_id"]).first()
        if existing:
            existing.first_name = row["first_name"]
            existing.last_name = row["last_name"]
            existing.email = row["email"]
            existing.phone = row.get("phone")
            existing.address = row.get("address")
            existing.date_of_birth = dob
            existing.account_balance = row.get("account_balance")
        else:
            created = None
            if row.get("created_at"):
                created = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
            db.add(Customer(
                customer_id=row["customer_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone=row.get("phone"),
                address=row.get("address"),
                date_of_birth=dob,
                account_balance=row.get("account_balance"),
                created_at=created,
            ))
        count += 1
    db.commit()
    return count
