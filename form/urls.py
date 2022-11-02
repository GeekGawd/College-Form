from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('form/<int:id>/', RegistrationFormView.as_view()),

    path('form/', PostRegistrationView.as_view()),

    path('form/list/', RegistrationListView.as_view(), name='form-list'),

    # path(r'signup/(?P<email>[\w-]+)/', SignUPView.as_view(), name = 'signup'),

    path('signup/verify/', SignUpOTPVerification.as_view(), name = 'signupverification'),

    path('signup/sendotp/', SignUpOTP.as_view(), name = 'sendotp'),

    path('reset/', PasswordResetOTP.as_view(), name='passwordreset'),

    path('reset/verify/', PasswordResetOTPConfirm.as_view(), name='passwordresetconfirmation'),

    path('reset/password/', ChangePassword.as_view(), name='passwordresetconfirmation'),

    path('token/', LoginAPIView.as_view(), name='token_obtain_pair'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('student/', StudentFormView.as_view(), name='StudentForm-view'),

    path('student/<int:id>/', StudentFormView.as_view(), name='StudentForm-view'),

    path('student/list/', StudentFormListView.as_view(), name='StudentForm-list-view'),

    path('student/import/', ImportStudentData.as_view(), name='StudentForm-list-view'),

    path('faculty-form/', FacultyParticipationFormView.as_view(), name='FacultyForm-view'),

    path('faculty-form/<int:id>/', FacultyParticipationFormView.as_view(), name='FacultyForm-view'),

    path('faculty-form/list/', FacultyParticipationFormListView.as_view(), name='FacultyForm-list-view'),

]