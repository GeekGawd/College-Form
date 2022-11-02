# Generated by Django 4.1.2 on 2022-11-02 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0021_remove_registration_unique registration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='face_to_face_fdp',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='incentive_detail',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='registration',
            name='online_fdp',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]