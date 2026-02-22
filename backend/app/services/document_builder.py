from app.models.entities import Contact, Opportunity


def mask_email(email: str | None) -> str:
    if not email or '@' not in email:
        return 'n/a'
    name, domain = email.split('@', 1)
    return f"{name[0]}***@{domain}"


def build_opportunity_document(op: Opportunity) -> tuple[str, dict]:
    content = (
        f"Opportunity {op.name} (Salesforce ID: {op.sf_id}). Stage: {op.stage_name}. "
        f"Amount: {op.amount}. Close date: {op.close_date}. Account: {op.account_name}. "
        f"Owner: {op.owner_name}. Last activity: {op.last_activity_date}."
    )
    metadata = {
        'name': op.name,
        'stage_name': op.stage_name,
        'amount': op.amount,
        'account_name': op.account_name,
        'owner_name': op.owner_name,
    }
    return content, metadata


def build_contact_document(contact: Contact) -> tuple[str, dict]:
    full_name = f"{contact.first_name or ''} {contact.last_name or ''}".strip()
    masked = mask_email(contact.email)
    content = (
        f"Contact {full_name} (Salesforce ID: {contact.sf_id}). Title: {contact.title}. "
        f"Email: {masked}. Account: {contact.account_name}. Last activity: {contact.last_activity_date}."
    )
    metadata = {
        'name': full_name,
        'title': contact.title,
        'email_masked': masked,
        'account_name': contact.account_name,
    }
    return content, metadata
