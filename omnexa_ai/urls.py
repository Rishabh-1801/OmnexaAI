"""
URL configuration for OMNEXA AI project.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Page views (SSR HTML or template renders)
    path('', include(('omnexa_ai.home.urls', 'home'), namespace='home')),
    path('services/', include(('omnexa_ai.services.urls', 'services'), namespace='services')),
    path('solutions/', include(('omnexa_ai.solutions.urls', 'solutions'), namespace='solutions')),
    path('case-studies/', include(('omnexa_ai.case_studies.urls', 'case_studies'), namespace='case_studies')),
    path('blog/', include(('omnexa_ai.blog.urls', 'blog'), namespace='blog')),
    path('about/', include(('omnexa_ai.about.urls', 'about'), namespace='about')),
    path('contact/', include(('omnexa_ai.contact.urls', 'contact'), namespace='contact')),
    path('careers/', include(('omnexa_ai.careers.urls', 'careers'), namespace='careers')),

    # REST API (all prefixed with /api/v1/)
    path('api/v1/contact/', include('omnexa_ai.contact.urls_api')),
    path('api/v1/services/', include('omnexa_ai.services.urls_api')),
    path('api/v1/solutions/', include('omnexa_ai.solutions.urls_api')),
    path('api/v1/case-studies/', include('omnexa_ai.case_studies.urls_api')),
    path('api/v1/blog/', include('omnexa_ai.blog.urls_api')),
    path('api/v1/chatbot/', include('omnexa_ai.chatbot.urls')),
    path('api/v1/careers/', include('omnexa_ai.careers.urls_api')),
    path('api/v1/home/', include('omnexa_ai.home.urls_api')),
]

# Always serve media files (even in production with DEBUG=False)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

