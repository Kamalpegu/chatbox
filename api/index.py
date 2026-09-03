from a_core.wsgi import application

class VercelWSGIMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Fix PATH_INFO on Vercel so Django receives user-requested route instead of /api/index.py
        request_uri = environ.get('REQUEST_URI', '')
        if request_uri:
            environ['PATH_INFO'] = request_uri.split('?')[0]
        elif environ.get('PATH_INFO', '').startswith('/api/index.py'):
            environ['PATH_INFO'] = '/'
        return self.app(environ, start_response)

app = VercelWSGIMiddleware(application)
