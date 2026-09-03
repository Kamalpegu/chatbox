import os
import sys

# Add the project root to sys.path so Django can find all modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')

from django.core.wsgi import get_wsgi_application
django_app = get_wsgi_application()


def application(environ, start_response):
    """
    Vercel WSGI entry point.
    Vercel passes the real URL in multiple environ keys.
    We restore PATH_INFO and QUERY_STRING from them.
    """
    # Vercel sets the original request path in these headers
    original_path = (
        environ.get('HTTP_X_FORWARDED_URI')        # preferred
        or environ.get('HTTP_X_NOW_URI')           # older Vercel
        or environ.get('REQUEST_URI')              # fallback
        or environ.get('PATH_INFO', '/')
    )

    # Strip query string from path
    if '?' in original_path:
        path, query = original_path.split('?', 1)
        environ['PATH_INFO'] = path
        environ['QUERY_STRING'] = query
    else:
        environ['PATH_INFO'] = original_path
        if 'QUERY_STRING' not in environ:
            environ['QUERY_STRING'] = ''

    # Safety: never let /api/index.py reach Django's URL router
    if environ['PATH_INFO'] in ('/api/index.py', '/api/index'):
        environ['PATH_INFO'] = '/'

    return django_app(environ, start_response)


app = application
