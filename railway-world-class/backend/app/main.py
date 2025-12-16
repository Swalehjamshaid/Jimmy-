
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db.session import async_session_factory
from app.api.v1.routes import auth, websites, audits, reports, health, admin, settings, verify

app = FastAPI(title="World-Class Web Audit SaaS", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(websites.router, prefix="/api/v1/websites", tags=["websites"])
app.include_router(audits.router, prefix="/api/v1/audits", tags=["audits"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(settings.router, prefix="/api/v1/settings", tags=["settings"])
app.include_router(verify.router, prefix="/api/v1/verify", tags=["verify"])

# Real-time audit progress websocket (simple polling of DB counts)
@app.websocket("/ws/audit-progress/{audit_run_id}")
async def audit_progress(ws: WebSocket, audit_run_id: int):
    await ws.accept()
    last = -1
    try:
        while True:
            async with async_session_factory() as session:
                cnt = (await session.execute(text("SELECT COUNT(*) FROM auditmetric WHERE audit_run_id=:rid"), {"rid": audit_run_id})).scalar()
                score = (await session.execute(text("SELECT score,status FROM auditrun WHERE id=:rid"), {"rid": audit_run_id})).first()
                await ws.send_json({"metrics": int(cnt or 0), "score": float(score[0] or 0), "status": score[1] if score else "unknown"})
            await asyncio.sleep(1)
    except Exception:
        await ws.close()
