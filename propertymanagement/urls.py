"""
URL configuration for propertymanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from userAccount.views import user_signup,user_login,social_redirect_view,profile_view,change_password,verify_otp,resend_otp
from userAccount.views import my_properties,add_my_property,edit_my_property,delete_my_property
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('userAccount.urls')),
    path('accounts/login/', user_login, name='login'),
    path('accounts/signup/', user_signup, name='signup'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', profile_view, name='profile'),
    path('profile/change_password/', change_password, name='change_password'),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path('resend-otp/', resend_otp, name='resend_otp'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('redirect-after-social-login/', social_redirect_view, name='social_redirect'),
    path('admin/', admin.site.urls),
    path('', include('proplistpage.urls')),  # Homepage and property views
    path('loan-calculator/', include('loan_calculator.urls')),
    path('payment/', include('payment.urls')),
    path('rent/', include('rentlistpage.urls')),
    path('my-properties/', my_properties, name='my_properties'),
    path('property/add/', add_my_property, name='add_my_property'),
    path('property/<int:pk>/edit/', edit_my_property, name='edit_my_property'),
    path('property/<int:pk>/delete/', delete_my_property, name='delete_my_property'),
    path('maintenance/', include('maintenance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
