# Generated by Django 3.0 on 2021-05-07 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Register', '0003_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='new',
            field=models.BooleanField(default=False),
        ),
    ]
