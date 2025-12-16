
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = '0001_init'
down_revision = None

def upgrade():
    op.create_table('organization', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(), nullable=False), sa.Column('subscription_plan', sa.String(), nullable=False, server_default='Free'))
    op.create_table('user', sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True), sa.Column('email', sa.String(), nullable=False, unique=True), sa.Column('password_hash', sa.String(), nullable=False), sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')), sa.Column('role', sa.String(), nullable=False, server_default='user'), sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organization.id'), nullable=False), sa.Column('created_at', sa.String(), nullable=False))
    op.create_table('website', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organization.id'), nullable=False), sa.Column('domain', sa.String(), nullable=False), sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')))
    op.create_table('auditrun', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('website_id', sa.Integer(), sa.ForeignKey('website.id'), nullable=False), sa.Column('score', sa.Float(), nullable=False, server_default='0'), sa.Column('status', sa.String(), nullable=False, server_default='pending'), sa.Column('started_at', sa.DateTime()), sa.Column('completed_at', sa.DateTime()))
    op.create_table('auditmetric', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('audit_run_id', sa.Integer(), sa.ForeignKey('auditrun.id'), nullable=False), sa.Column('category', sa.String(), nullable=False), sa.Column('metric_name', sa.String(), nullable=False), sa.Column('value', sa.String()), sa.Column('score', sa.Float(), nullable=False, server_default='0'), sa.Column('recommendation', sa.Text()))
    op.create_table('report', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('audit_run_id', sa.Integer(), sa.ForeignKey('auditrun.id'), nullable=False), sa.Column('type', sa.String(), nullable=False), sa.Column('file_url', sa.String(), nullable=False))

def downgrade():
    for t in ['report','auditmetric','auditrun','website','user','organization']:
        op.drop_table(t)
