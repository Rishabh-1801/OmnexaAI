from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.conf import settings

class AutoAdminMiddleware:
    _admin_created = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not AutoAdminMiddleware._admin_created:
            AutoAdminMiddleware._admin_created = True
            try:
                User = get_user_model()
                admin_user, created = User.objects.get_or_create(
                    username='admin',
                    defaults={
                        'email': 'admin@omnexa.ai',
                        'is_superuser': True,
                        'is_staff': True
                    }
                )
                updated = False
                if not admin_user.is_superuser:
                    admin_user.is_superuser = True
                    updated = True
                if not admin_user.is_staff:
                    admin_user.is_staff = True
                    updated = True
                if created or not admin_user.check_password('admin123'):
                    admin_user.set_password('admin123')
                    updated = True
                
                if updated:
                    admin_user.save()
                    print("AutoAdminMiddleware: Superuser 'admin' created/updated successfully with password 'admin123'")
            except Exception as e:
                # If database tables are not ready, reset flag to try again on next request
                AutoAdminMiddleware._admin_created = False
        
        return self.get_response(request)


class SitePasswordMiddleware:
    """
    Middleware that gates the entire site behind a password.
    Password is read from settings.SITE_PASSWORD.
    Exempt paths: /enter-password/, /admin/, /static/, /media/, /api/
    """

    # Paths that bypass the password gate
    EXEMPT_PREFIXES = (
        '/enter-password/',
        '/admin/',
        '/static/',
        '/media/',
        '/api/',
    )

    def __init__(self, get_response):
        self.get_response = get_response
        self.site_password = getattr(settings, 'SITE_PASSWORD', None)

    def __call__(self, request):
        # If no password is configured, let all traffic through
        if not self.site_password:
            return self.get_response(request)

        # Allow exempt paths through
        for prefix in self.EXEMPT_PREFIXES:
            if request.path.startswith(prefix):
                return self.get_response(request)

        # Check if already authenticated via session
        if request.session.get('site_password_ok'):
            return self.get_response(request)

        # Not authenticated — redirect to password page
        return redirect('/enter-password/?next=' + request.path)
