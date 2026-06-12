# Deployment Guide

**Recommended: Deploy entire Django + Channels app to Render (Option A).**

See [RENDER_SETUP.md](RENDER_SETUP.md) for step-by-step instructions.

## Quick Summary

- Deploy backend (Django + Channels + Daphne) to **Render** using the `Procfile`.
- Use Redis for `CHANNEL_LAYERS` and set `REDIS_URL` environment variable.
- Attach PostgreSQL database via Render.
- Static files served by Django.
- No Vercel needed.

## Why Option A?

1. **Simpler**: Everything on one host (Render)
2. **Cheaper**: One service = lower cost
3. **No build issues**: Python dependencies work out-of-the-box
4. **Django templates work**: No need to separate frontend/backend

## Environment Variables (Render)

```
SECRET_KEY=<generate-new>
DEBUG=False
ALLOWED_HOSTS=chatbox.onrender.com
DATABASE_URL=<auto-set by Render>
REDIS_URL=<auto-set by Render>
```

See [RENDER_SETUP.md](RENDER_SETUP.md) for full instructions.



## Environment variables (backend)
- `SECRET_KEY` (required) — use `python manage.py shell` → `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`
- `DEBUG=False`
- `ALLOWED_HOSTS` (comma separated)
- `DATABASE_URL` (Postgres)
- `REDIS_URL` (Redis)

## Local Testing

1. Install: `pip install -r requirements.txt`
2. Create `.env` with `SECRET_KEY`, `DEBUG=True`, `REDIS_URL` (optional for local testing)
3. Migrate: `python manage.py migrate`
4. Run: `python manage.py runserver`


## Troubleshooting

### Build fails with "psycopg2-binary"
- Should be fixed in latest code. Redeploy.

### WebSocket not connecting
- Ensure backend is running and REDIS_URL is set.
- Check `ALLOWED_HOSTS` includes your Render domain.
- Check logs on Render for errors.

### Database not found
- Ensure `DATABASE_URL` is set on Render.
- Verify PostgreSQL service is attached.
- Run migrations: `python manage.py migrate`.

## Notes
- Use Render free tier for testing ($0/month).
- Upgrade to **Starter** plan ($7/month) for production stability.
- Static files served by Django.

