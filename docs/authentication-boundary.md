# Authentication boundary

WordPress or a future OpenID Connect provider owns credentials, login sessions,
password changes, password resets, and optional multi-factor authentication.
FastAPI never receives or stores a user password.

The local `users` table is an authorization mapping. It stores:

- the trusted identity provider
- the provider's stable user identifier (`external_subject`)
- the membership role
- an optional link to a GDCF member
- whether backend access is active
- audit timestamps

WordPress website roles and FastAPI membership roles are separate. A WordPress
webmaster does not automatically receive access to sensitive membership data.
FastAPI membership roles are `member`, `membership_staff`, and
`membership_admin`.

Before accepting identity claims, FastAPI must validate a signed, short-lived
token from the configured provider. Browser-provided role headers or raw
WordPress user IDs must never be trusted directly.
