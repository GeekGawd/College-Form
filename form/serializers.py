from dataclasses import field
from rest_framework import serializers
from form.models import FacultyParticipationForm, Registration, User, StudentForm
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
import re, itertools
from django.contrib.auth import authenticate
from datetime import datetime


class StartingDateField(serializers.Field):

    def to_representation(self, start_date):
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime("%d-%m-%Y")
        else:
            start_date = start_date.strftime("%d-%m-%Y")
        return start_date

    def to_internal_value(self, start_date):
        start_date = datetime.strptime(start_date, "%d-%m-%Y").strftime('%Y-%m-%d')
        return start_date

class EndDateField(serializers.Field):

    def to_representation(self, end_date):
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime("%d-%m-%Y")
        else:
            end_date = end_date.strftime("%d-%m-%Y")
        return end_date

    def to_internal_value(self, end_date):
        end_date = datetime.strptime(end_date, "%d-%m-%Y").strftime('%Y-%m-%d')
        return end_date


class RegistrationSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    starting_date = StartingDateField()
    end_date = EndDateField()

    class Meta:
        model = Registration
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        data = self.context['request'].data
        user.college_email = validated_data['college_email']
        user.phone_number = validated_data['phone_number']
        user.name = validated_data['name']
        user.department = validated_data['department']
        user.designation = validated_data['designation']
        user.save()
        validated_data['starting_date'] = datetime.strptime(data['starting_date'], "%d-%m-%Y").strftime('%Y-%m-%d')
        validated_data['end_date'] = datetime.strptime(data['end_date'], "%d-%m-%Y").strftime('%Y-%m-%d')
        return super().create(validated_data)

    def get_is_admin(self, instance):
        request = self.context['request']
        return request.user.is_superuser
    
    def validate_face_to_face_fdp(self, face_to_face_fdp):
        request = self.context['request']
        fdp_type = request.data.get('fdp_type', None)
        online_fdp = request.data.get('online_fdp', None)

        if fdp_type == "Face to Face FDP" and online_fdp != "" and online_fdp is not None:
            raise serializers.ValidationError("FDP Name doesn't match with FDP Type")
        
        if fdp_type == "Face to Face FDP" and (face_to_face_fdp is None or face_to_face_fdp == ""):
            raise serializers.ValidationError("Face to Face FDP Name cannot be Null")
        return face_to_face_fdp

    def validate_online_fdp(self, online_fdp):
        request = self.context['request']
        fdp_type = request.data.get('fdp_type', None)
        face_to_face_fdp = request.data.get('face_to_face_fdp', None)

        if fdp_type == "Online" and face_to_face_fdp is not None and face_to_face_fdp != "":
            raise serializers.ValidationError("FDP Name doesn't match with FDP Type")
        
        if fdp_type == "Online" and (online_fdp is None or online_fdp == ""):
            raise serializers.ValidationError("Online FDP Name cannot be Null")

        return online_fdp

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
    starting_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = StudentForm
        fields = '__all__'

    def create(self, validated_data):
        data = self.context['request'].data
        validated_data['starting_date'] = datetime.strptime(data['starting_date'], "%d-%m-%Y").strftime('%Y-%m-%d')
        validated_data['end_date'] = datetime.strptime(data['end_date'], "%d-%m-%Y").strftime('%Y-%m-%d')
        return super().create(validated_data)
    
    def get_is_admin(self, instance):
        request = self.context['request']
        return request.user.is_superuser
    
    def get_starting_date(self, instance):
        start_date = instance.starting_date
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime("%d-%m-%Y")
        else:
            start_date = start_date.strftime("%d-%m-%Y")
        return start_date

    
    def get_end_date(self, instance):
        end_date = instance.end_date
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime("%d-%m-%Y")
        else:
            end_date = end_date.strftime("%d-%m-%Y")
        return end_date


class FacultyParticipationFormSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    starting_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    class Meta:
        model = FacultyParticipationForm
        fields = '__all__'

    def create(self, validated_data):
        data = self.context['request'].data
        validated_data['starting_date'] = datetime.strptime(data['starting_date'], "%d-%m-%Y").strftime('%Y-%m-%d')
        validated_data['end_date'] = datetime.strptime(data['end_date'], "%d-%m-%Y").strftime('%Y-%m-%d')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        data = self.context['request'].data
        validated_data['starting_date'] = datetime.strptime(data['starting_date'], "%d-%m-%Y").strftime('%Y-%m-%d')
        validated_data['end_date'] = datetime.strptime(data['end_date'], "%d-%m-%Y").strftime('%Y-%m-%d')
        return super().update(instance, validated_data)
    
    def get_is_admin(self, instance):
        request = self.context['request']
        return request.user.is_superuser
    
    def get_starting_date(self, instance):
        start_date = instance.starting_date
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime("%d-%m-%Y")
        else:
            start_date = start_date.strftime("%d-%m-%Y")
        return start_date

    
    def get_end_date(self, instance):
        end_date = instance.end_date
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime("%d-%m-%Y")
        else:
            end_date = end_date.strftime("%d-%m-%Y")
        return end_date

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

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['college_email', 'phone_number', 'name', 'department', 'designation']