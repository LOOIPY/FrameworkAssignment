"""
URL configuration for userAccount app.
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
app_name = 'userAccount'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('property/add/', views.add_my_property, name='add_my_property'),
    path('property/<int:pk>/edit/', views.edit_my_property, name='edit_my_property'),
    path('property/<int:pk>/delete/', views.delete_my_property, name='delete_my_property'),
<<<<<<< HEAD
=======
    path('property/<int:property_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('saved/', views.saved_properties, name='saved_properties'),
    path('ajax/toggle-favorite/', views.ajax_toggle_favorite, name='ajax_toggle_favorite'),
>>>>>>> Pei-Yi
]

# Add media static file support (only in DEBUG mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)