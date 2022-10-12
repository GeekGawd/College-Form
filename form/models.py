from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    college_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=10,
                                    validators=[RegexValidator(regex='^[0-9]{10}$', message='Enter a 10 digit phone number.',),], null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def refresh(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh)
    
    def access(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def get_name(self):
        return str(self.name)
    
    def is_admin(self):
        return self.is_superuser


class OTP(models.Model):
    otp = models.IntegerField()
    otp_email = models.EmailField()
    time_created = models.IntegerField()
    
    def __str__(self):
        return f"{self.otp_email} : {self.otp}"


DEPARTMENTS = [
                ("Applied Sciences & Humanities", "Applied Sciences & Humanities"),
                ("Electronics And Communication Engineering", "Electronics And Communication Engineering"),
                ("Mechanical Engineering", "Mechanical Engineering"),
                ("Civil Engineering", "Civil Engineering"),
                ("Electrical And Electronics Engineering", "Electrical And Electronics Engineering"),
                ("Computer Science And Engineering", "Computer Science And Engineering"),
                ("Information Technology", "Information Technology"),
                ("Master Of Computer Applications", "Master Of Computer Applications")
            ]
FDP_TYPE = [
    ("Face to Face FDP", "Face to Face FDP"),
    ("Online", "Online")
]

INCENTIVE_DETAILS = [
    ("AKTU Level-2 (10,000)", "AKTU Level-2 (10,000)"),
    ("AKTU Level-3 (15,000)", "AKTU Level-3 (15,000)"),
    ("AICTE UHV-III (10,000)", "AICTE UHV-III (10,000)"),
    ("AICTE UHV-IV (15,000)", "AICTE UHV-IV (15,000)"),
    ("Not Taken Yet", "Not Taken Yet"),
]

FACE_TO_FACE_FDP = [
    ("AKTU Level-1", "AKTU Level-1"),
    ("AKTU Refresher", "AKTU Refresher"),
    ("AKTU Level-2", "AKTU Level-2"),
    ("AKTU Level-3", "AKTU Level-3"),
    ("AKTU 10 days FDP on UHBC", "AKTU 10 days FDP on UHBC"),
    ("AKTU 10 days FDP on VREHC", "AKTU 10 days FDP on VREHC"),
    ("AKTU 10 days FDP on HVMD", "AKTU 10 days FDP on HVMD"),
    ("AICTE UHV-II", "AICTE UHV-II"),
    ("AICTE UHV-III", "AICTE UHV-III"),
    ("AICTE UHV-IV", "AICTE UHV-IV")
]

ONLINE_FDP = [
    ("AICTE-UHV Refresher Part-I", "AICTE-UHV Refresher Part-I"),
    ("AICTE-UHV Refresher Part-II", "AICTE-UHV Refresher Part-II"),
    ("AICTE-5 Day Online UHV-I", "AICTE-5 Day Online UHV-I"),
    ("AICTE-6 Day Online UHV-II", "AICTE-6 Day Online UHV-II"),
    ("AKTU-HV in Shankya and Vedant Darshan (eight days)", "AKTU-HV in Shankya and Vedant Darshan (eight days)"),
    ("AKTU-HV in Jain and Baudh Darshan (eight days)", "AKTU-HV in Jain and Baudh Darshan (eight days)")
]

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college_email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=10,
                                    validators=[RegexValidator(regex='^[0-9]{10}$', message='Enter a 10 digit phone number.',),], null = True)
    name = models.CharField(max_length=250)
    department = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)
    fdp_type = models.CharField(
        max_length=50,
        choices=FDP_TYPE
    )
    face_to_face_fdp = models.CharField(
                                        max_length=200, 
                                        choices=FACE_TO_FACE_FDP,
                                        blank=True,
                                        null=True
                                        )
    online_fdp = models.CharField(
                                max_length=200,
                                choices=ONLINE_FDP,
                                blank=True,
                                null=True
                                )
    starting_date = models.DateField()
    end_date = models.DateField()
    number_of_days = models.PositiveBigIntegerField()
    venue = models.CharField(max_length=250)
    certificate_number = models.CharField(max_length=250)
    certificate = models.FileField()
    incentive_detail = models.CharField(
        max_length=50,
        choices=INCENTIVE_DETAILS
    )
    remarks = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name','department','college_email','phone_number','starting_date','end_date','certificate_number','incentive_detail','venue'], name='unique registration')
        ]

class StudentForm(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    roll_no = models.CharField(max_length=15)
    course = models.CharField(max_length=55)
    branch = models.CharField(max_length=255)
    year = models.CharField(max_length=25)
    section = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10,
                                    validators=[RegexValidator(regex='^[0-9]{10}$', message='Enter a 10 digit phone number.',),], null = True)
    name_of_activity = models.CharField(max_length=255)
    venue_of_activity = models.CharField(max_length=255)
    number_of_days = models.CharField(blank=True, null=True, max_length = 50)
    starting_date = models.DateField()
    end_date = models.DateField()
    remarks = models.TextField()

class FacultyParticipationForm(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10,
                                    validators=[RegexValidator(regex='^[0-9]{10}$', message='Enter a 10 digit phone number.',),], null = True)
    name_of_event = models.CharField(max_length=255)
    venue_of_activity = models.CharField(max_length=255)
    duration = models.PositiveBigIntegerField()
    starting_date = models.DateField()
    end_date = models.DateField()
    remarks = models.TextField()
