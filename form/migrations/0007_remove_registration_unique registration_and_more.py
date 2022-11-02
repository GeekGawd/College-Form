# Generated by Django 4.1.1 on 2022-10-10 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0006_remove_registration_unique registration_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='registration',
            name='unique registration',
        ),
        migrations.AddConstraint(
            model_name='registration',
            constraint=models.UniqueConstraint(fields=('college_email', 'phone_number', 'fdp_type'), name='unique registration'),
        ),
    ]
