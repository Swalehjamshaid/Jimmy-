
from alembic import op
import sqlalchemy as sa
revision = '0004_activity'
down_revision = '0003_ext'

def upgrade():
    op.create_table('useractivity', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.String(), nullable=False), sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organization.id'), nullable=False), sa.Column('action', sa.String(), nullable=False), sa.Column('details', sa.String()), sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')))
    op.execute("ALTER TABLE useractivity ENABLE ROW LEVEL SECURITY;")
    op.execute("CREATE POLICY org_isolation_useractivity ON useractivity USING (organization_id::text = current_setting('app.current_organization_id', true));")

def downgrade():
    op.execute("DROP TABLE IF EXISTS useractivity CASCADE;")
