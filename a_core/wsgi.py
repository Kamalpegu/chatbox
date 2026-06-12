import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbox.settings')

application = get_wsgi_application()
app = application  # Vercel needs this line to find the app instance
