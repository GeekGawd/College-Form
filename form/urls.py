from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('form/', RegistrationFormView.as_view()),

    path('signup/', SignUPView.as_view()),

    path('reset/', PasswordResetOTP.as_view(), name='passwordreset'),

    path('reset/verify/', PasswordResetOTPConfirm.as_view(), name='passwordresetconfirmation'),

    path('reset/password/', ChangePassword.as_view(), name='passwordresetconfirmation'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]