# Generated by Django 4.1.1 on 2022-10-15 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0017_alter_facultyparticipationform_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='certificate',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]