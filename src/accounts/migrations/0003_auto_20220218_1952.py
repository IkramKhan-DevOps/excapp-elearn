# Generated by Django 3.2.8 on 2022-02-18 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220131_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_customer',
            new_name='is_student',
        ),
        migrations.AddField(
            model_name='user',
            name='is_instructor',
            field=models.BooleanField(default=False),
        ),
    ]
