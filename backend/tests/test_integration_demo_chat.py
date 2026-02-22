from types import SimpleNamespace

from app.services.chat import generate_chat_response


class FakeDB:
    pass


def test_demo_chat_returns_citations(monkeypatch):
    docs = [
        SimpleNamespace(source_type='opportunity', source_sf_id='006D1', content='Opportunity Acme Renewal stage Negotiation', metadata_json={'name': 'Acme Renewal'}),
        SimpleNamespace(source_type='contact', source_sf_id='003D1', content='Contact Alice Buyer email a***@acme.com', metadata_json={'name': 'Alice Buyer'}),
    ]

    monkeypatch.setattr('app.services.chat.retrieve_documents', lambda db, tenant_id, message, top_k=6: docs)
    resp = generate_chat_response(FakeDB(), 'tenant', 'What is happening?')
    assert len(resp['citations']) >= 1
    assert resp['citations'][0]['source_sf_id'] == '006D1'
