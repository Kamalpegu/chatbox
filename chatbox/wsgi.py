import os
import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

# 1. First, point Django to your settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbox.settings')

# 2. Force Django to initialize and load the settings configurations completely
django.setup()

# 3. Now that settings are loaded safely, trigger your database migrations
call_command("migrate", interactive=False)

# 4. Hand off the core process back to the standard Vercel live server instance
application = get_wsgi_application()
