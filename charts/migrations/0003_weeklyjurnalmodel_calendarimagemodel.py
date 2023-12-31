# Generated by Django 4.2.4 on 2023-09-13 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('charts', '0002_hourssleptmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyJurnalModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accomplished', models.TextField(default='', max_length=255)),
                ('optional', models.TextField(default='', max_length=255)),
                ('really_well', models.TextField(default='', max_length=255)),
                ('differently', models.TextField(default='', max_length=255)),
                ('learn', models.TextField(default='', max_length=255)),
                ('date', models.DateField()),
                ('select_call', models.CharField(choices=[('1', 'Call săptămânal - Structură de decizie "if" / "else"'), ('2', 'Call săptămânal - Structuri repetitive "while" / "for"'), ('3', 'Call săptămânal - "Șiruri de numere"'), ('4', 'Call săptămânal - "Matrice (Tablouri bidimensionale)"'), ('5', 'Call săptămânal - Mindset'), ('6', 'Call săptămânal - Simulări de interviuri'), ('7', 'Call săptămânal - Proiecte personale')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'date')},
            },
        ),
        migrations.CreateModel(
            name='CalendarImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar', models.ImageField(upload_to='charts/images')),
                ('jurnal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charts.weeklyjurnalmodel')),
            ],
        ),
    ]
