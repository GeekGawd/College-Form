from rest_framework import serializers
from form.models import FacultyParticipationForm, Registration, User, StudentForm
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
import re, itertools
from django.contrib.auth import authenticate



class RegistrationSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    class Meta:
        model = Registration
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def get_is_admin(self, instance):
        request = self.context['request']
        return request.user.is_superuser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']
        extra_kwargs = {
                        'email': {'required': True, 'error_messages': {"required": "Email field may not be blank."}},
                       }
    
    def validate_email(self, email):
        if not re.findall("[a-zA-Z0-9]+(@akgec.ac.in)", email):
            raise ValidationError(
                ("Enter a Valid College Email ID"),
                code='invalid_email',
            )
        return email

    def create(self, validated_data):
        email = validated_data['email']
        password = email.split('@akgec.ac.in')[0] + "@1234"
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()

        # Send password to the user on their email
        subject = "Login Credentials for College Form"
        msg = EmailMessage(subject, f'<div> Here are the login credentials:</div><div>Email: {email}</div><div>Password: {password}</div>', 'collegeform.contact@gmail.com', (email,))
        msg.content_subtype = "html"

        msg.send()

        return user
    
    def to_representation(self,instance):
        data = super(UserSerializer, self).to_representation(instance)
        data['access']=instance.access()
        data['refresh']=instance.refresh()
        return data

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, password):
        if not re.findall('\d', password):
            raise ValidationError(
                ("The password must contain at least 1 digit, 0-9."),
                code='password_no_number',
            )
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                ("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )
        if not re.findall('[a-z]', password):
            raise ValidationError(
                ("The password must contain at least 1 lowercase letter, a-z."),
                code='password_no_lower',
            )

        return password

class StudentFormSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    class Meta:
        model = StudentForm
        fields = '__all__'
    
    def get_is_admin(self, instance):
        request = self.context['request']
        return request.user.is_superuser

class FacultyParticipationFormSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    class Meta:
        model = FacultyParticipationForm
        fields = '__all__'
    
    def get_is_admin(self, instance):
        request = self.context['request']
        return request.user.is_superuser

class AuthTokenSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, error_messages={
                                  "required": "Email field may not be blank."}, write_only=True)
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = User
        fields = ['email', 'access', 'refresh', 'password', 'is_admin']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['is_admin'] = instance.is_superuser
    #     return data

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            raise ValidationError(
                'Unable to authenticate with provided credentials')

        return {
            'refresh': user.refresh,
            'access': user.access,
            'is_admin': user.is_superuser
        } 