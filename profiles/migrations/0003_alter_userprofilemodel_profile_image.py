# Generated by Django 4.2 on 2024-05-08 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_userprofilemodel_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='profile_image',
            field=models.ImageField(blank=True, default='defaultuser.png', null=True, upload_to='profiles/photos'),
        ),
    ]
