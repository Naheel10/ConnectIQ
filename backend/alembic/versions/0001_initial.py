"""initial
"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    op.create_table('tenants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id')),
        sa.Column('email', sa.String(length=255), unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
    )
    op.create_table('salesforce_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), unique=True),
        sa.Column('access_token', sa.Text(), nullable=False),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('instance_url', sa.Text(), nullable=False),
        sa.Column('issued_at', sa.DateTime(), nullable=False),
    )
    op.create_table('opportunities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id')),
        sa.Column('sf_id', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('stage_name', sa.String(length=120)),
        sa.Column('amount', sa.Float()),
        sa.Column('close_date', sa.Date()),
        sa.Column('account_name', sa.String(length=255)),
        sa.Column('owner_name', sa.String(length=255)),
        sa.Column('last_activity_date', sa.Date()),
        sa.Column('raw_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('updated_at_sf', sa.DateTime()),
        sa.Column('embedded_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('tenant_id', 'sf_id', name='uq_opp_tenant_sf'),
    )
    op.create_table('contacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id')),
        sa.Column('sf_id', sa.String(length=50), nullable=False),
        sa.Column('first_name', sa.String(length=120)),
        sa.Column('last_name', sa.String(length=120)),
        sa.Column('email', sa.String(length=255)),
        sa.Column('title', sa.String(length=255)),
        sa.Column('account_name', sa.String(length=255)),
        sa.Column('last_activity_date', sa.Date()),
        sa.Column('raw_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('updated_at_sf', sa.DateTime()),
        sa.Column('embedded_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('tenant_id', 'sf_id', name='uq_contact_tenant_sf'),
    )
    op.create_table('documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id')),
        sa.Column('source_type', sa.String(length=20), nullable=False),
        sa.Column('source_sf_id', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('embedding', Vector(1536)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('tenant_id', 'source_type', 'source_sf_id', name='uq_doc_source'),
    )
    op.create_table('sync_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id')),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('finished_at', sa.DateTime()),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('error', sa.Text()),
        sa.Column('opportunities_upserted', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('contacts_upserted', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('documents_upserted', sa.Integer(), nullable=False, server_default='0'),
    )


def downgrade() -> None:
    op.drop_table('sync_runs')
    op.drop_table('documents')
    op.drop_table('contacts')
    op.drop_table('opportunities')
    op.drop_table('salesforce_tokens')
    op.drop_table('users')
    op.drop_table('tenants')
