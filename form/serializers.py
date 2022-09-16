from rest_framework import serializers
from form.models import Registration, User
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
import re


class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Registration
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

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
        password = User.objects.make_random_password()
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        email = validated_data.pop('email')

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