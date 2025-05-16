from django.contrib import admin
from django.urls import path, include
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # your app api
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('auth/social/login/', GoogleLogin.as_view(), name='google_login'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    # JWT token endpoints if using JWT
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
]