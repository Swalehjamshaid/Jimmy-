
# app/main.py
from fastapi import FastAPI
from .models import Base
from .db import engine
from .routers import auth, orgs, sites, audits, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SaaS Web Audit")
app.include_router(auth.router)
app.include_router(orgs.router)
app.include_router(sites.router)
app.include_router(audits.router)
app.include_router(reports.router)

@app.get("/health")
def health():
    return {"status": "ok"}
