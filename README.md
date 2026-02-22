# ConnectIQ

Production-grade demo web app that syncs Salesforce Opportunities + Contacts into Postgres, embeds with pgvector/OpenAI, and answers pipeline questions via RAG with strict citations.

## Quick start
1. Copy env file: `cp .env.example .env`
2. Run app: `docker compose up --build`
3. Open frontend: http://localhost:5173
4. Login with `DEMO_USER_EMAIL` / `DEMO_USER_PASSWORD` (default: `demo@connectiq.com`)

## Demo mode
- Default sync uses demo Salesforce-like records when real OAuth token is not configured.
- In **Setup**, keep `Demo mode` checked and click **Run Sync**.
- Ask questions on **Chat** and inspect citations.

## Salesforce setup (local OAuth demo)
1. Create Salesforce connected app with OAuth enabled.
2. Set callback URL to `http://localhost:8000/salesforce/oauth/callback`.
3. Put client ID/secret in `.env`.
4. In Setup, click **Connect Salesforce** and complete login.
5. Run sync with `Demo mode` unchecked.

## Example questions
- “What is my forecast by stage?”
- “Which deals look at risk this month?”
- “Who are key contacts on Acme opportunities?”

## Architecture
```
[React/Vite UI]
   | /api
[FastAPI]
   |-- Auth + OAuth
   |-- Sync runner (Salesforce or demo)
   |-- RAG chat (LangChain + OpenAI)
   |
[Postgres + pgvector]
   |-- opportunities/contacts (normalized + raw_json)
   |-- documents (embedding vector)
   |-- sync_runs (observability)
```

## Resume bullets
- Built end-to-end Salesforce-to-RAG analytics platform with incremental sync and vector search on PostgreSQL/pgvector.
- Implemented grounded conversational analytics with strict per-record citations for auditability.
- Delivered fully containerized DX (`docker compose up --build`) with demo-mode fallback requiring no external credentials.


## Common Issues
- If login fails, verify `DEMO_USER_EMAIL` / `DEMO_USER_PASSWORD` in `.env` and restart containers (`docker compose up --build`).
- The demo seed is idempotent and updates the configured demo user password on startup, so changing `.env` does not require a volume wipe.
- To fully reset DB state, run `docker compose down -v` and then `docker compose up --build`.
