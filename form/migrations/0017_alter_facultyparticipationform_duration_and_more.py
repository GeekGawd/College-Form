# Generated by Django 4.1.1 on 2022-10-12 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0016_alter_registration_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facultyparticipationform',
            name='duration',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='registration',
            name='number_of_days',
            field=models.CharField(max_length=50),
        ),
    ]