# Generated by Django 4.1.7 on 2023-03-28 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_user_email_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_verified',
            new_name='is_verified',
        ),
    ]