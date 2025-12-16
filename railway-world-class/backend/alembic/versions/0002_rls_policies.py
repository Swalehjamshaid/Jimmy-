
from alembic import op
revision = '0002_rls'
down_revision = '0001_init'

def upgrade():
    for tbl in ['organization','website','auditrun','auditmetric','report']:
        op.execute(f"ALTER TABLE {tbl} ENABLE ROW LEVEL SECURITY;")
    op.execute("""
    CREATE POLICY org_isolation_organization ON organization USING (id::text = current_setting('app.current_organization_id', true));
    """)
    op.execute("""
    CREATE POLICY org_isolation_website ON website USING (organization_id::text = current_setting('app.current_organization_id', true));
    """)
    op.execute("""
    CREATE POLICY org_isolation_auditrun ON auditrun USING ((SELECT organization_id FROM website WHERE website.id=auditrun.website_id)::text = current_setting('app.current_organization_id', true));
    """)
    op.execute("""
    CREATE POLICY org_isolation_auditmetric ON auditmetric USING ((SELECT organization_id FROM website JOIN auditrun ON auditrun.id=auditmetric.audit_run_id WHERE website.id=auditrun.website_id)::text = current_setting('app.current_organization_id', true));
    """)
    op.execute("""
    CREATE POLICY org_isolation_report ON report USING ((SELECT organization_id FROM website JOIN auditrun ON auditrun.id=report.audit_run_id WHERE website.id=auditrun.website_id)::text = current_setting('app.current_organization_id', true));
    """)

def downgrade():
    op.execute("DROP POLICY IF EXISTS org_isolation_report ON report;")
    op.execute("DROP POLICY IF EXISTS org_isolation_auditmetric ON auditmetric;")
    op.execute("DROP POLICY IF EXISTS org_isolation_auditrun ON auditrun;")
    op.execute("DROP POLICY IF EXISTS org_isolation_website ON website;")
    op.execute("DROP POLICY IF EXISTS org_isolation_organization ON organization;")
    for tbl in ['organization','website','auditrun','auditmetric','report']:
        op.execute(f"ALTER TABLE {tbl} DISABLE ROW LEVEL SECURITY;")
