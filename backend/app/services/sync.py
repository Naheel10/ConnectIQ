from datetime import date, datetime, timezone

from simple_salesforce import Salesforce
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.entities import Contact, Document, Opportunity, SalesforceToken, SyncRun
from app.services.document_builder import build_contact_document, build_opportunity_document
from app.services.embeddings import embed_text
from app.utils.security import decrypt_value

settings = get_settings()


def _demo_records():
    now = datetime.now(timezone.utc)
    opps = [
        {'Id': '006D0000001', 'Name': 'Acme Renewal', 'StageName': 'Negotiation/Review', 'Amount': 120000, 'CloseDate': str(date.today()), 'Account': {'Name': 'Acme Corp'}, 'Owner': {'Name': 'Jane Seller'}, 'LastActivityDate': str(date.today()), 'LastModifiedDate': now.isoformat()},
        {'Id': '006D0000002', 'Name': 'Globex Expansion', 'StageName': 'Prospecting', 'Amount': 85000, 'CloseDate': str(date.today()), 'Account': {'Name': 'Globex'}, 'Owner': {'Name': 'John AE'}, 'LastActivityDate': str(date.today()), 'LastModifiedDate': now.isoformat()},
    ]
    contacts = [
        {'Id': '003D0000001', 'FirstName': 'Alice', 'LastName': 'Buyer', 'Email': 'alice@acme.com', 'Title': 'VP Procurement', 'Account': {'Name': 'Acme Corp'}, 'LastActivityDate': str(date.today()), 'LastModifiedDate': now.isoformat()},
        {'Id': '003D0000002', 'FirstName': 'Bob', 'LastName': 'Champion', 'Email': 'bob@globex.com', 'Title': 'Director IT', 'Account': {'Name': 'Globex'}, 'LastActivityDate': str(date.today()), 'LastModifiedDate': now.isoformat()},
    ]
    return opps, contacts


def _fetch_salesforce(db: Session, tenant_id):
    token = db.scalar(select(SalesforceToken).where(SalesforceToken.tenant_id == tenant_id))
    if not token:
        return _demo_records()
    sf = Salesforce(instance_url=token.instance_url, session_id=decrypt_value(token.access_token))
    opp_query = "SELECT Id, Name, StageName, Amount, CloseDate, LastActivityDate, LastModifiedDate, Account.Name, Owner.Name FROM Opportunity"
    con_query = "SELECT Id, FirstName, LastName, Email, Title, LastActivityDate, LastModifiedDate, Account.Name FROM Contact"
    return sf.query_all(opp_query)['records'], sf.query_all(con_query)['records']


def run_sync(db: Session, tenant_id, demo_mode: bool = True) -> SyncRun:
    run = SyncRun(tenant_id=tenant_id, status='running', started_at=datetime.utcnow())
    db.add(run)
    db.commit()
    db.refresh(run)
    try:
        opp_records, con_records = _demo_records() if demo_mode else _fetch_salesforce(db, tenant_id)
        run.opportunities_upserted = _upsert_opportunities(db, tenant_id, opp_records)
        run.contacts_upserted = _upsert_contacts(db, tenant_id, con_records)
        run.documents_upserted = _upsert_documents(db, tenant_id)
        run.status = 'success'
    except Exception as exc:
        run.status = 'failed'
        run.error = str(exc)
    finally:
        run.finished_at = datetime.utcnow()
        db.add(run)
        db.commit()
    return run


def _to_dt(val):
    if not val:
        return None
    return datetime.fromisoformat(str(val).replace('Z', '+00:00'))


def _upsert_opportunities(db: Session, tenant_id, records: list[dict]) -> int:
    count = 0
    for r in records:
        obj = db.scalar(select(Opportunity).where(Opportunity.tenant_id == tenant_id, Opportunity.sf_id == r['Id']))
        if not obj:
            obj = Opportunity(tenant_id=tenant_id, sf_id=r['Id'], raw_json=r, name=r.get('Name') or '')
        obj.name = r.get('Name') or ''
        obj.stage_name = r.get('StageName')
        obj.amount = r.get('Amount')
        obj.close_date = r.get('CloseDate')
        obj.account_name = (r.get('Account') or {}).get('Name') if isinstance(r.get('Account'), dict) else None
        obj.owner_name = (r.get('Owner') or {}).get('Name') if isinstance(r.get('Owner'), dict) else None
        obj.last_activity_date = r.get('LastActivityDate')
        obj.updated_at_sf = _to_dt(r.get('LastModifiedDate'))
        obj.raw_json = r
        db.add(obj)
        count += 1
    db.commit()
    return count


def _upsert_contacts(db: Session, tenant_id, records: list[dict]) -> int:
    count = 0
    for r in records:
        obj = db.scalar(select(Contact).where(Contact.tenant_id == tenant_id, Contact.sf_id == r['Id']))
        if not obj:
            obj = Contact(tenant_id=tenant_id, sf_id=r['Id'], raw_json=r)
        obj.first_name = r.get('FirstName')
        obj.last_name = r.get('LastName')
        obj.email = r.get('Email')
        obj.title = r.get('Title')
        obj.account_name = (r.get('Account') or {}).get('Name') if isinstance(r.get('Account'), dict) else None
        obj.last_activity_date = r.get('LastActivityDate')
        obj.updated_at_sf = _to_dt(r.get('LastModifiedDate'))
        obj.raw_json = r
        db.add(obj)
        count += 1
    db.commit()
    return count


def _upsert_documents(db: Session, tenant_id) -> int:
    count = 0
    for op in db.execute(select(Opportunity).where(Opportunity.tenant_id == tenant_id)).scalars().all():
        doc = db.scalar(select(Document).where(Document.tenant_id == tenant_id, Document.source_type == 'opportunity', Document.source_sf_id == op.sf_id))
        should_embed = not op.embedded_at or (op.updated_at_sf and op.embedded_at and op.updated_at_sf > op.embedded_at)
        if should_embed:
            content, metadata = build_opportunity_document(op)
            if not doc:
                doc = Document(tenant_id=tenant_id, source_type='opportunity', source_sf_id=op.sf_id, content=content, metadata_json=metadata)
            doc.content = content
            doc.metadata_json = metadata
            doc.embedding = embed_text(content)
            op.embedded_at = datetime.utcnow()
            db.add(doc)
            db.add(op)
            count += 1
    for c in db.execute(select(Contact).where(Contact.tenant_id == tenant_id)).scalars().all():
        doc = db.scalar(select(Document).where(Document.tenant_id == tenant_id, Document.source_type == 'contact', Document.source_sf_id == c.sf_id))
        should_embed = not c.embedded_at or (c.updated_at_sf and c.embedded_at and c.updated_at_sf > c.embedded_at)
        if should_embed:
            content, metadata = build_contact_document(c)
            if not doc:
                doc = Document(tenant_id=tenant_id, source_type='contact', source_sf_id=c.sf_id, content=content, metadata_json=metadata)
            doc.content = content
            doc.metadata_json = metadata
            doc.embedding = embed_text(content)
            c.embedded_at = datetime.utcnow()
            db.add(doc)
            db.add(c)
            count += 1
    db.commit()
    return count
