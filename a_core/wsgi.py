import os
import sys
from django.core.wsgi import get_wsgi_application

# Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbox.settings') # <-- Make sure this matches your project name!

# Get the WSGI application
application = get_wsgi_application()

# ---- AUTO-MIGRATION TRICK FOR VERCEL ----
try:
    from django.core.management import call_command
    print("Running auto-migrations on database...")
    call_command('migrate', interactive=False)
    print("Migrations completed successfully!")
except Exception as e:
    print(f"Migration failed during startup: {e}", file=sys.stderr)
# -----------------------------------------
