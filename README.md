# Backend Assessment - Customer Data Pipeline

3 services: Flask mock API → FastAPI ingestion → PostgreSQL.

## Run

```bash
docker-compose up -d
```

Give it ~10 sec for postgres to be ready, then ingest:

```bash
curl -X POST http://localhost:8000/api/ingest
```

## Test

Flask (mock data):
```bash
curl "http://localhost:5000/api/customers?page=1&limit=5"
curl "http://localhost:5000/api/customers/cust_001"
curl "http://localhost:5000/api/health"
```

FastAPI (DB):
```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
curl "http://localhost:8000/api/customers/cust_001"
```

## Structure

- **mock-server** – Flask on 5000, serves JSON from `data/customers.json`
- **pipeline-service** – FastAPI on 8000, ingests from Flask into postgres
- **postgres** – DB on 5432
