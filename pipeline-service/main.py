from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, init_db
from models.customer import Customer
from services.ingestion import fetch_all, upsert_batch

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/api/ingest")
def ingest(db: Session = Depends(get_db)):
    try:
        rows = fetch_all()
        count = upsert_batch(db, rows)
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Customer)
    total = q.count()
    offset = (page - 1) * limit
    data = q.offset(offset).limit(limit).all()
    return {
        "data": [
            {
                "customer_id": c.customer_id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address,
                "date_of_birth": str(c.date_of_birth) if c.date_of_birth else None,
                "account_balance": float(c.account_balance) if c.account_balance else None,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in data
        ],
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    c = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "customer_id": c.customer_id,
        "first_name": c.first_name,
        "last_name": c.last_name,
        "email": c.email,
        "phone": c.phone,
        "address": c.address,
        "date_of_birth": str(c.date_of_birth) if c.date_of_birth else None,
        "account_balance": float(c.account_balance) if c.account_balance else None,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }
