
import os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
url = os.getenv('DATABASE_URL')
if not url: raise SystemExit('DATABASE_URL not set')
if url.startswith('postgresql://'): url = url.replace('postgresql://','postgresql+psycopg2://')
engine = create_engine(url, pool_pre_ping=True)
orgs = [{"name":"Acme Corp","plan":"Pro"}]
with Session(engine) as s:
    for org in orgs:
        oid = s.execute(text('INSERT INTO organization (name, subscription_plan) VALUES (:n,:p) RETURNING id'), {"n":org['name'],"p":org['plan']}).scalar()
        s.execute(text("SELECT set_config('app.current_organization_id', :org, false);"), {"org": str(oid)})
        now = datetime.utcnow().isoformat()
        s.execute(text('INSERT INTO "user" (id,email,password_hash,is_verified,role,organization_id,created_at) VALUES (gen_random_uuid(),:e,:ph,true,:r,:oid,:now)'), {"e":"admin@acme.demo","ph":"$2b$12$SeEdPlAcEhOlDeRhAsH","r":"admin","oid":oid,"now":now})
        s.execute(text('INSERT INTO website (organization_id, domain, is_active) VALUES (:oid,:dom,true)'), {"oid":oid, "dom":"acme.example"})
    s.commit()
print('Seed complete')
