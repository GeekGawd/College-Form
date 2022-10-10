# Generated by Django 4.1.1 on 2022-10-10 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0004_remove_registration_unique appversion_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='registration',
            name='unique registration',
        ),
        migrations.AddConstraint(
            model_name='registration',
            constraint=models.UniqueConstraint(fields=('college_email', 'phone_number', 'fdp_type', 'face_to_face_fdp', 'online_fdp', 'starting_date', 'end_date', 'venue', 'certificate_number', 'incentive_detail'), name='unique registration'),
        ),
    ]
