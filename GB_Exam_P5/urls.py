from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from usersapp import views as usersapp_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipesiteapp.urls')),
    path('register/', usersapp_views.register, name='register'),
    path('profile/', usersapp_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='usersapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='usersapp/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
