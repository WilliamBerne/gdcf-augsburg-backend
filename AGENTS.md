# GDCF Augsburg Backend - Agent Guidance

## Project priorities

- Treat the local working tree as the source of truth; project summaries may lag behind it.
- Finish and stabilize the membership-management backend before starting frontend, OCR, or broad DevOps work.
- Prefer coherent, reviewable changes. Group closely related updates, verify the complete batch, and pause when a decision or broader scope needs user review.
- Do not reorganize working code unless the current task clearly requires it.

## Before changing code

- Inspect the relevant routes, schemas, models, migrations, and tests first.
- Check `git status` and preserve unrelated user changes.
- State the intended small change and its scope.

## Backend conventions

- Keep FastAPI routes thin; extract reusable business logic only when duplication or complexity justifies it.
- Use dependency injection for database sessions and future authentication.
- Use explicit Pydantic request and response schemas with clear type hints.
- Validate input at the API boundary and return consistent HTTP errors.
- Handle database integrity errors with rollback; do not expose them as unhandled HTTP 500 responses.
- Prefer member archival/deactivation over permanent deletion when record retention matters.

## Database and security

- Preserve Alembic history. Never edit or delete an existing migration casually.
- Create a new migration for schema changes and describe its upgrade and downgrade effects.
- Never commit `.env`, credentials, tokens, passwords, uploaded member documents, or real member data.
- Tests must use isolated configuration and must not modify production data.

## Verification and handoff

- Add or update focused tests for behavior changes.
- Run the narrowest relevant tests first; report commands and results.
- At each review checkpoint, list modified files, explain any migration impact, and suggest only the next small step.
