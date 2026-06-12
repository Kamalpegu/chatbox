# Deployment Guide

This project uses Django + Channels (Daphne) for WebSockets and should be deployed with an ASGI-compatible host for the backend and Vercel (or similar) for the frontend static site.

## Summary
- Deploy backend (Django + Channels + Daphne) to Render/Fly/Heroku/DO Apps using the `Procfile` or `Dockerfile`.
- Use Redis for `CHANNEL_LAYERS` and set `REDIS_URL` environment variable on the backend host.
- Deploy frontend (static files or Next.js) to Vercel and configure API rewrites for HTTP; connect WebSocket directly to backend `wss://` URL.

## ⚠️ Important: Do NOT deploy to Vercel serverless
Vercel is a serverless platform and **cannot run Daphne/Channels** for persistent WebSocket connections. Each function has a 10-second timeout. Deploy the backend to a proper ASGI host (Render, Fly, Heroku, Railway, etc.).

## Step 1: Set up backend on Render

### Create a Render service
1. Go to [render.com](https://render.com) and sign up.
2. Click **New** → **Web Service**.
3. Connect your GitHub repo `Kamalpegu/chatbox`.
4. Configure:
   - **Name**: `chatbox-backend`
   - **Environment**: Python 3.11
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `daphne -b 0.0.0.0 -p $PORT a_core.asgi:application`

### Add environment variables (in Render service settings)
```
SECRET_KEY=<generate a new secret key>
DEBUG=False
ALLOWED_HOSTS=chatbox-backend.onrender.com,your-vercel-domain.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-vercel-domain.vercel.app
DATABASE_URL=<Render Postgres connection URL>
REDIS_URL=<Render Redis connection URL>
```

### Add Postgres and Redis
1. Create a **PostgreSQL database** in Render (attach to the service).
2. Create a **Redis** instance in Render (attach to the service).
3. Copy `DATABASE_URL` and `REDIS_URL` from the attachments into environment variables.

## Step 2: Deploy frontend to Vercel

### Create Vercel project
1. Go to [vercel.com](https://vercel.com).
2. Click **Add New Project** → Import from GitHub → select `chatbox`.
3. Set **Root Directory** to `.` (or `frontend/` if you separate frontend later).
4. **Skip** environment variables for now (frontend doesn't need Django secrets).
5. Deploy.

### Configure frontend to call backend
In your frontend templates or JavaScript, update API/WebSocket URLs:

- **HTTP API calls**: `https://your-vercel-domain.vercel.app/api/...` (rewritten to backend via `vercel.json`)
- **WebSocket**: `wss://chatbox-backend.onrender.com/ws/chatroom/public-chat` (direct to backend)

### Example JavaScript (chat.html or frontend)
```javascript
// WebSocket connection
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsURL = `${protocol}//chatbox-backend.onrender.com/ws/chatroom/public-chat`;
const ws = new WebSocket(wsURL);
```

## Step 3: Configure `vercel.json` for API rewrites
Update `vercel.json` to proxy HTTP API calls to the backend:

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://chatbox-backend.onrender.com/api/$1" }
  ]
}
```

**Note**: WebSocket connections must go directly to the backend domain (cannot be proxied through Vercel).

## Environment variables (backend)
- `SECRET_KEY` (required) — use `python manage.py shell` → `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`
- `DEBUG=False`
- `ALLOWED_HOSTS` (comma separated)
- `DATABASE_URL` (Postgres)
- `REDIS_URL` (Redis)

## Local testing before deploy
1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file locally with test values (see `.env.example`).
3. Run migrations: `python manage.py migrate`
4. Test WebSocket: `python manage.py runserver`

## Troubleshooting

### "Serverless Function Crashed" on Vercel
**This is expected.** Django Channels cannot run on Vercel serverless. Deploy the backend to Render/Heroku/etc. instead.

### WebSocket connection refused
- Ensure backend is running and REDIS_URL is set.
- Check firewall/security group allows port 443 (WSS).
- Verify `ALLOWED_HOSTS` includes your frontend domain.

### Database not found
- Ensure `DATABASE_URL` is set on the backend host.
- Run migrations on the backend: `python manage.py migrate --noinput` (add to Render deploy hook or manually run once).
