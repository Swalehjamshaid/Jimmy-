
from alembic import op
import sqlalchemy as sa
revision = '0003_ext'
down_revision = '0002_rls'

def upgrade():
    op.create_table('verificationtoken', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.String(), sa.ForeignKey('user.id'), nullable=False), sa.Column('token', sa.String(), nullable=False), sa.Column('expires_at', sa.DateTime(), nullable=False), sa.Column('used', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.create_table('subscription', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organization.id'), nullable=False), sa.Column('plan', sa.String(), nullable=False), sa.Column('stripe_customer_id', sa.String()), sa.Column('stripe_subscription_id', sa.String()), sa.Column('valid_until', sa.DateTime()))
    op.create_table('auditthreshold', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organization.id'), nullable=False), sa.Column('category', sa.String(), nullable=False), sa.Column('min_score', sa.Float(), nullable=False, server_default='70'))
    op.create_table('orgsettings', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organization.id'), nullable=False), sa.Column('brand_name', sa.String()), sa.Column('brand_color', sa.String()))
    for tbl in ['subscription','auditthreshold','orgsettings']:
        op.execute(f"ALTER TABLE {tbl} ENABLE ROW LEVEL SECURITY;")
        op.execute(f"CREATE POLICY org_isolation_{tbl} ON {tbl} USING (organization_id::text = current_setting('app.current_organization_id', true));")

def downgrade():
    for tbl in ['orgsettings','auditthreshold','subscription','verificationtoken']:
        op.execute(f"DROP TABLE IF EXISTS {tbl} CASCADE;")
