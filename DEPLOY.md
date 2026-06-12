# Deployment Guide

This project uses Django + Channels (Daphne) for WebSockets and should be deployed with an ASGI-compatible host for the backend and Vercel (or similar) for the frontend static site.

## Summary
- Deploy backend (Django + Channels + Daphne) to Render/Fly/Heroku/DO Apps using the `Procfile` or `Dockerfile`.
- Use Redis for `CHANNEL_LAYERS` and set `REDIS_URL` environment variable on the backend host.
- Deploy frontend (static files or Next.js) to Vercel and configure API rewrites for HTTP; connect WebSocket directly to backend `wss://` URL.

## Environment variables (backend)
- `SECRET_KEY` (required)
- `DEBUG=false`
- `ALLOWED_HOSTS` (comma separated or set in platform UI)
- `DATABASE_URL` or configure Postgres via provider
- `REDIS_URL` (redis://:<password>@<host>:6379)

## Example steps (Render)
1. Create a new web service on Render.
2. Connect the GitHub repo `Kamalpegu/chatbox`.
3. Set build and start commands (or use Dockerfile):

Build command: `pip install -r requirements.txt`
Start command (if not using Dockerfile): `daphne -b 0.0.0.0 -p $PORT a_core.asgi:application`

4. Add environment variables listed above.
5. Configure persistent store (Postgres) and Redis addon.

## Vercel (frontend)
- Add `vercel.json` rewrites for HTTP API calls to the backend domain.
- For WebSocket, configure the frontend to connect directly to `wss://your-backend-domain/ws/...`.

## Notes
- Do not run the Channels worker on Vercel (serverless) — use a full backend host.
- Test locally using the same `REDIS_URL` as production if possible.
