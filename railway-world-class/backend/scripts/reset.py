
import os, sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
DEMO_ORG = 'Acme Corp'
confirm = '--confirm' in sys.argv
if not confirm and '--dry-run' not in sys.argv:
    print('Add --confirm to execute or --dry-run to preview'); sys.exit(1)
url = os.getenv('DATABASE_URL');
if not url: print('DATABASE_URL not set'); sys.exit(1)
if url.startswith('postgresql://'): url = url.replace('postgresql://','postgresql+psycopg2://')
engine = create_engine(url, pool_pre_ping=True)
with Session(engine) as s:
    row = s.execute(text('SELECT id FROM organization WHERE name=:n'), {"n": DEMO_ORG}).first()
    if not row:
        print('Demo org not found'); sys.exit(0)
    oid = row[0]
    s.execute(text("SELECT set_config('app.current_organization_id', :org, false);"), {"org": str(oid)})
    steps = [
        "DELETE FROM auditmetric USING auditrun WHERE auditmetric.audit_run_id=auditrun.id AND auditrun.website_id IN (SELECT id FROM website WHERE organization_id=:oid)",
        "DELETE FROM report USING auditrun WHERE report.audit_run_id=auditrun.id AND auditrun.website_id IN (SELECT id FROM website WHERE organization_id=:oid)",
        "DELETE FROM auditrun WHERE website_id IN (SELECT id FROM website WHERE organization_id=:oid)",
        "DELETE FROM website WHERE organization_id=:oid",
        "DELETE FROM "user" WHERE organization_id=:oid",
        "DELETE FROM organization WHERE id=:oid",
    ]
    for sql in steps:
        print('Exec:', sql)
        if confirm:
            s.execute(text(sql), {"oid": oid})
    if confirm:
        s.commit()
print('Reset done')
