# Generated by Django 4.2.4 on 2023-10-08 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendsrequestmodel',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
