
from fastapi import APIRouter, Depends
from sqlalchemy import select
from app.core.deps import get_db_with_org, get_current_user
from app.db.models.report import Report

router = APIRouter()

@router.get('/')
async def list_reports(user=Depends(get_current_user), db=Depends(get_db_with_org)):
    res = await db.execute(select(Report))
    items = res.scalars().all()
    return [{"id": r.id, "type": r.type, "file_url": r.file_url} for r in items]
