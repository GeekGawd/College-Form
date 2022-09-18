from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('form/', RegistrationFormView.as_view()),

    path('form/list/', RegistrationListView.as_view(), name='form-list'),

    # path(r'signup/(?P<email>[\w-]+)/', SignUPView.as_view(), name = 'signup'),

    path('signup/verify/', SignUpOTPVerification.as_view(), name = 'signupverification'),

    path('signup/sendotp/', SignUpOTP.as_view(), name = 'sendotp'),

    path('reset/', PasswordResetOTP.as_view(), name='passwordreset'),

    path('reset/verify/', PasswordResetOTPConfirm.as_view(), name='passwordresetconfirmation'),

    path('reset/password/', ChangePassword.as_view(), name='passwordresetconfirmation'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]