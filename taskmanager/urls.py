from django.contrib import admin
from django.urls import path, include
from core.views import GoogleLogin, github_auth, RegisterView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # your app api

    # REST auth routes
    path('auth/registration/', RegisterView.as_view(), name='auth_registration'),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),

    # Social login with Google (token-based)
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/github/', github_auth, name='github_auth'),

    # JWT token endpoints (optional, can be used separately)
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
]
