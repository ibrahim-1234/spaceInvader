# Generated by Django 4.1.4 on 2022-12-29 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userPage', '0004_alter_userinfo_email_alter_userinfo_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
