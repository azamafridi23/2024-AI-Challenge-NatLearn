from django.urls import path
from . import views
from .views import  CombinedView
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('combined/', CombinedView.as_view(), name='combined_view'),
    path('combined/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',

    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
        ), name='password_reset_complete'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
