# Generated by Django 4.2.4 on 2023-12-26 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_seen_friendsrequestmodel_accepted_seen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendsrequestmodel',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
