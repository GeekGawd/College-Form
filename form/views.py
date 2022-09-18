from urllib import request
from django.shortcuts import render
from rest_framework import generics, mixins, parsers, status
from rest_framework.response import Response
from form.models import Registration, User
from form.serializers import RegistrationSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from form.models import OTP
import random
from django.core.mail import EmailMessage
import time
from django.http import Http404
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse



# Create your views here.

def send_otp_email(email,subject):
    
    OTP.objects.filter(otp_email__iexact = email).delete()

    otp = random.randint(1000,9999)

    msg = EmailMessage(subject, f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:2em;color: #FFD243;text-decoration:none;font-weight:600">College Form</a></div><p style="font-size:1.2em">Greetings,</p><p style="font-size:1.2em"> Looks like you forgot your password. No worries we are here to help you recover your account. Use the following OTP to recover your account<br><b style="text-align: center;display: block;">Note: OTP is only valid for 5 minutes.</b></p><h2 style="font-size: 1.9em;background: #FFD243;margin: 0 auto;width: max-content;padding: 0 15px;color: #fff;border-radius: 4px;">{otp}</h2><p style="font-size:1.2em;">Regards,<br/>Team Software Incubator</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:1.2em;line-height:1;font-weight:500"><p>College Form</p><p> 3rd Floor CSIT Block, AKGEC</p><p>Ghaziabad</p></div></div></div>' , 'collegeform.contact@gmail.com', (email,))
    msg.content_subtype = "html"
    msg.send()

    time_created = int(time.time())

    OTP.objects.create(otp=otp, otp_email = email, time_created = time_created)
    return "Reset Mail Sent"

def send_login_mail(email, subject):

    OTP.objects.filter(otp_email__iexact = email).delete()

    otp = random.randint(1000,9999)

    msg = EmailMessage(subject, f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:2em;color: #FFD243;text-decoration:none;font-weight:600">College Form</a></div><p style="font-size:1.2em">Greetings,</p><p style="font-size:1.2em"> Use the following OTP to complete your Sign Up procedures<br><b style="text-align: center;display: block;">Note: OTP is only valid for 5 minutes.</b></p><h2 style="font-size: 1.9em;background: #FFD243;margin: 0 auto;width: max-content;padding: 0 15px;color: #fff;border-radius: 4px;">{otp}</h2><p style="font-size:1.2em;">Regards,<br/>Team Software Incubator</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:1.2em;line-height:1;font-weight:500"><p>Connect</p><p>3rd Floor CSIT Block, AKGEC</p><p>Ghaziabad</p></div></div></div>', 'collegeform.contact@gmail.com', (email,))
    msg.content_subtype = "html"
    msg.send()

    time_created = int(time.time())
    OTP.objects.create(otp=otp, otp_email = email, time_created = time_created)
    
    return "Email Sent"

# class SignUPView(generics.CreateAPIView):
#     permission_classes = [AllowAny]
#     model = User
#     serializer_class = UserSerializer
#     def post(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)

class PasswordResetOTP(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request_email = request.data.get("email", )

        try:
            user = User.objects.get(email__iexact = request_email)
        except:
            return Response({"status" : "No such account exists"},status = status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            send_otp_email(request_email,"[OTP] Password Change for College Form")
            return Response({"status" : "OTP has been sent to your email."}, status = status.HTTP_200_OK)
        return Response({"status": "Please verify your account."}, status=status.HTTP_406_NOT_ACCEPTABLE)

class PasswordResetOTPConfirm(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self,request):
        request_otp   = request.data.get("otp",)
        request_email = request.data.get("email",)

        if request_email:
            try:
                otp_instance = OTP.objects.get(otp_email__iexact = request_email)
                user = User.objects.get(email__iexact = request_email)
            except:
                raise Http404

            request_time = otp_instance.time_created
            email = otp_instance.otp_email
            current_time = int(time.time())

            if current_time - request_time > 300:
                return Response({"status" : "Sorry, entered OTP has expired.", "entered otp": request_otp},status = status.HTTP_408_REQUEST_TIMEOUT)

            if str(otp_instance.otp) != str(request_otp):
                 return Response({"status" : "Sorry, entered OTP doesn't match the sent OTP."},status = status.HTTP_409_CONFLICT)

            if (request_email != email):
                return Response({"status" : "Sorry, entered OTP doesn't belong to your email id."},status = status.HTTP_401_UNAUTHORIZED)

            return Response({"status": "OTP has been verified.", "access_token": user.access()}, status=status.HTTP_200_OK)

        return Response({"status": "Please Provide an email address"},status = status.HTTP_400_BAD_REQUEST)

class ChangePassword(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):

        try:
            user = request.user
        except:
            return Response({"status": "Given User email is not registered." },
                                status=status.HTTP_403_FORBIDDEN)
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if check_password(request.data.get("new_password",), user.password):
                return Response({"status": "New password cannot be the same as old password." },
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(user.tokens(),status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationFormView(
                        generics.GenericAPIView,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin
                            ):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    permission_classes = [IsAuthenticated]
    serializer_class = RegistrationSerializer
    def get_object(self):
        form_id = self.kwargs['id']
        return Registration.objects.get(id=form_id, user = self.request.user)
    
    def get(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({"status": "No Form Found"}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class PostRegistrationView(generics.CreateAPIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    permission_classes = [IsAuthenticated]
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        request.data.update({"user":request.user.id})
        return super().create(request, *args, **kwargs)

class RegistrationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)

class SignUpOTP(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request):
        request_email = request.data.get("email",)
        try:
            user = User.objects.get(email__iexact = request_email)
            return Response({"status": "User is already registered."}, status=status.HTTP_403_FORBIDDEN)
        except:
            if request_email:
                send_login_mail(request_email, "[OTP] New Login for College Form")
                return Response({'status':'OTP sent successfully.'},status = status.HTTP_200_OK)
            else:
                return Response({"status":"Please enter an email id"},status = status.HTTP_400_BAD_REQUEST)

class SignUpOTPVerification(generics.GenericAPIView,
                            mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    model = User
    serializer_class = UserSerializer

    def post(self, request):

        request_otp   = request.data.get("otp",)
        request_email = request.data.get("email")
        if request_email:
            try:
                otp_instance = OTP.objects.get(otp_email__iexact = request_email)
            except:
                raise Http404

        otp = otp_instance.otp
        email = otp_instance.otp_email

        request_time = OTP.objects.get(otp_email__iexact = request_email).time_created
        current_time = int(time.time())

        if current_time - request_time > 300:
            return Response({"status" : "Sorry, entered OTP has expired."}, status = status.HTTP_403_FORBIDDEN)

        if str(request_otp) == str(otp) and request_email == email:
            OTP.objects.filter(otp_email__iexact = request_email).delete()
            return super().create(request)
        else:
            return Response({
                'status':'OTP incorrect.'
            }, status=status.HTTP_400_BAD_REQUEST)