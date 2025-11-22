from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500
from destinations import views as destination_views

# Admin site customization
admin.site.site_header = 'Tourist Destination Manager Admin'
admin.site.site_title = 'Tourist Destination Manager'
admin.site.index_title = 'Administration'

# Error handlers
handler404 = 'destinations.views.handler404'
handler500 = 'destinations.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', destination_views.home, name='home'),
    path('destinations/', include('destinations.urls', namespace='destinations')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)