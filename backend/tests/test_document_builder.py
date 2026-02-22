from types import SimpleNamespace

from app.services.document_builder import build_contact_document, build_opportunity_document, mask_email


def test_mask_email():
    assert mask_email('john@example.com') == 'j***@example.com'


def test_document_templates_include_key_fields():
    opp = SimpleNamespace(sf_id='0061', name='Deal A', stage_name='Prospecting', amount=1000, close_date='2025-01-01', account_name='Acme', owner_name='Jane', last_activity_date='2025-01-02')
    content, metadata = build_opportunity_document(opp)
    assert 'Deal A' in content
    assert metadata['stage_name'] == 'Prospecting'

    contact = SimpleNamespace(sf_id='0031', first_name='Alice', last_name='Smith', title='VP', email='alice@acme.com', account_name='Acme', last_activity_date='2025-01-03')
    ccontent, cmeta = build_contact_document(contact)
    assert 'A***@acme.com'.lower() in ccontent.lower()
    assert cmeta['email_masked'].startswith('a***')
