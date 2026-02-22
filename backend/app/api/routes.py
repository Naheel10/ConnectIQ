from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy import desc, or_, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_tenant_id
from app.core.config import get_settings
from app.db.session import get_db
from app.models.entities import Contact, Opportunity, SalesforceToken, SyncRun, User
from app.schemas.api import ChatRequest, ChatResponse, LoginRequest
from app.services.chat import generate_chat_response
from app.services.sync import run_sync
from app.utils.security import create_access_token, encrypt_value, verify_password

router = APIRouter()
settings = get_settings()


@router.get('/health')
def health(db: Session = Depends(get_db)):
    db.execute(select(1))
    return {'status': 'ok'}


@router.post('/auth/login')
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return {'token': create_access_token(user.email)}


@router.get('/salesforce/oauth/start')
def sf_oauth_start():
    params = urlencode({
        'response_type': 'code',
        'client_id': settings.salesforce_client_id,
        'redirect_uri': settings.salesforce_redirect_uri,
    })
    return RedirectResponse(url=f"{settings.salesforce_login_url}/services/oauth2/authorize?{params}")


@router.get('/salesforce/oauth/callback')
def sf_oauth_callback(code: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    import httpx

    resp = httpx.post(
        f"{settings.salesforce_login_url}/services/oauth2/token",
        data={
            'grant_type': 'authorization_code',
            'client_id': settings.salesforce_client_id,
            'client_secret': settings.salesforce_client_secret,
            'redirect_uri': settings.salesforce_redirect_uri,
            'code': code,
        },
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    token = db.scalar(select(SalesforceToken).where(SalesforceToken.tenant_id == user.tenant_id))
    if not token:
        token = SalesforceToken(tenant_id=user.tenant_id, access_token='', instance_url='')
    token.access_token = encrypt_value(data['access_token'])
    token.refresh_token = encrypt_value(data.get('refresh_token', '')) if data.get('refresh_token') else None
    token.instance_url = data['instance_url']
    db.add(token)
    db.commit()
    return RedirectResponse(url=f"{settings.frontend_url}/setup")


@router.post('/sync/run')
def sync_run(demo_mode: bool = True, tenant_id=Depends(get_tenant_id), db: Session = Depends(get_db)):
    run = run_sync(db, tenant_id, demo_mode=demo_mode)
    return {'status': run.status, 'run_id': str(run.id)}


@router.get('/sync/status')
def sync_status(tenant_id=Depends(get_tenant_id), db: Session = Depends(get_db)):
    run = db.scalar(select(SyncRun).where(SyncRun.tenant_id == tenant_id).order_by(desc(SyncRun.started_at)).limit(1))
    if not run:
        return {'status': 'never'}
    return {
        'status': run.status,
        'started_at': run.started_at,
        'finished_at': run.finished_at,
        'counts': {
            'opportunities': run.opportunities_upserted,
            'contacts': run.contacts_upserted,
            'documents': run.documents_upserted,
        },
        'error': run.error,
    }


@router.post('/chat', response_model=ChatResponse)
def chat(payload: ChatRequest, tenant_id=Depends(get_tenant_id), db: Session = Depends(get_db)):
    return generate_chat_response(db, tenant_id, payload.message)


@router.get('/records/opportunities')
def opportunities(
    limit: int = 20,
    q: str | None = None,
    stage: str | None = None,
    owner: str | None = None,
    tenant_id=Depends(get_tenant_id),
    db: Session = Depends(get_db),
):
    query = select(Opportunity).where(Opportunity.tenant_id == tenant_id)
    if q:
        query = query.where(or_(Opportunity.name.ilike(f'%{q}%'), Opportunity.account_name.ilike(f'%{q}%')))
    if stage:
        query = query.where(Opportunity.stage_name == stage)
    if owner:
        query = query.where(Opportunity.owner_name == owner)
    rows = db.execute(query.order_by(desc(Opportunity.updated_at_sf)).limit(limit)).scalars().all()
    return rows


@router.get('/records/contacts')
def contacts(
    limit: int = 20,
    q: str | None = None,
    account: str | None = None,
    tenant_id=Depends(get_tenant_id),
    db: Session = Depends(get_db),
):
    query = select(Contact).where(Contact.tenant_id == tenant_id)
    if q:
        query = query.where(or_(Contact.first_name.ilike(f'%{q}%'), Contact.last_name.ilike(f'%{q}%'), Contact.email.ilike(f'%{q}%')))
    if account:
        query = query.where(Contact.account_name == account)
    rows = db.execute(query.order_by(desc(Contact.updated_at_sf)).limit(limit)).scalars().all()
    return rows
