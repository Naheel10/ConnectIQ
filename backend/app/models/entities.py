import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Tenant(Base):
    __tablename__ = 'tenants'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), default='default')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tenants.id'))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))


class SalesforceToken(Base):
    __tablename__ = 'salesforce_tokens'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tenants.id'), unique=True)
    access_token: Mapped[str] = mapped_column(Text)
    refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    instance_url: Mapped[str] = mapped_column(Text)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Opportunity(Base):
    __tablename__ = 'opportunities'
    __table_args__ = (UniqueConstraint('tenant_id', 'sf_id', name='uq_opp_tenant_sf'),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tenants.id'))
    sf_id: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(255))
    stage_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    close_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    account_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    owner_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_activity_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    raw_json: Mapped[dict] = mapped_column(JSON)
    updated_at_sf: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    embedded_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Contact(Base):
    __tablename__ = 'contacts'
    __table_args__ = (UniqueConstraint('tenant_id', 'sf_id', name='uq_contact_tenant_sf'),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tenants.id'))
    sf_id: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    account_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_activity_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    raw_json: Mapped[dict] = mapped_column(JSON)
    updated_at_sf: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    embedded_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Document(Base):
    __tablename__ = 'documents'
    __table_args__ = (UniqueConstraint('tenant_id', 'source_type', 'source_sf_id', name='uq_doc_source'),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tenants.id'))
    source_type: Mapped[str] = mapped_column(String(20))
    source_sf_id: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column('metadata', JSON)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SyncRun(Base):
    __tablename__ = 'sync_runs'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tenants.id'))
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20))
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    opportunities_upserted: Mapped[int] = mapped_column(Integer, default=0)
    contacts_upserted: Mapped[int] = mapped_column(Integer, default=0)
    documents_upserted: Mapped[int] = mapped_column(Integer, default=0)
