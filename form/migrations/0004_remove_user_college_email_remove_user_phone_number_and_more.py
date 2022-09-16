# Generated by Django 4.1.1 on 2022-09-16 11:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_remove_registration_college_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='college_email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='registration',
            name='college_email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='phone_number',
            field=models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a 10 digit phone number.', regex='^[0-9]{10}$')]),
        ),
    ]
