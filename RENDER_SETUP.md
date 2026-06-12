# Render Deployment Guide (Option A)

Deploy the entire Django + Channels app to Render. This is the simplest approach.

## Step 1: Create Render Account
Go to [render.com](https://render.com) and sign up with GitHub.

## Step 2: Create Web Service
1. Click **New** → **Web Service**
2. Select repo: `Kamalpegu/chatbox`
3. Fill in:
   - **Name**: `chatbox` (or any name)
   - **Environment**: `Python 3.11`
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `daphne -b 0.0.0.0 -p $PORT a_core.asgi:application`
   - **Instance type**: Free tier (or Starter+ for production)

## Step 3: Add PostgreSQL Database
1. In Render dashboard, click **New** → **PostgreSQL**
2. **Name**: `chatbox-db`
3. **PostgreSQL Version**: 15
4. **Pricing Plan**: Free tier
5. Create
6. Copy `Internal Database URL` — you'll need this

## Step 4: Add Redis
1. Click **New** → **Redis**
2. **Name**: `chatbox-redis`
3. **Pricing Plan**: Free tier
4. Create
5. Copy `Internal Redis URL` — you'll need this

## Step 5: Attach Database & Redis to Service
1. Go back to your Web Service (`chatbox`)
2. Go to **Environment** tab
3. Add:
   - `DATABASE_URL`: Paste the PostgreSQL Internal URL
   - `REDIS_URL`: Paste the Redis Internal URL
4. Save

## Step 6: Set Django Environment Variables
In the same **Environment** tab, add:

```
SECRET_KEY=<generate-new>
DEBUG=False
ALLOWED_HOSTS=chatbox.onrender.com
```

To generate `SECRET_KEY`, run locally:
```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Then copy-paste the output into the `SECRET_KEY` field.

## Step 7: Deploy
1. Click **Manual Deploy** → **Deploy latest commit**
2. Wait for build (5-10 minutes)
3. Check **Logs** for errors

## Step 8: Run Migrations (first time only)
After first deploy, run migrations:

1. Open the Web Service
2. Click **Shell** (top right)
3. Run: `python manage.py migrate`
4. Exit

## Step 9: Access Your App
Your app is live at: `https://chatbox.onrender.com`

## Troubleshooting

### Build fails with "psycopg2-binary"
- This is fixed in the latest code. Redeploy.

### WebSocket not connecting
- Check `ALLOWED_HOSTS` includes your domain
- Ensure Redis URL is set and accessible
- Check logs for errors

### Database/Redis not found
- Verify `DATABASE_URL` and `REDIS_URL` are set
- Check they're **Internal** URLs (not public)
- Redeploy after updating

## Notes
- Free tier services pause after 15 minutes of inactivity
- For production, upgrade to **Starter** plan ($7/month)
- Static files are served by Django (you can add S3 later for scalability)
