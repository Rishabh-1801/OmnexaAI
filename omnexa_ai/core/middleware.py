from django.contrib.auth import get_user_model

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
