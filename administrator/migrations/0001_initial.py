# Generated by Django 4.2.4 on 2024-06-04 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caller_name', models.CharField(max_length=100)),
                ('caller_phone', models.IntegerField()),
                ('time_of_call', models.DateTimeField(auto_now_add=True)),
                ('priority', models.CharField(choices=[('Highest', 'highest'), ('Moderate', 'moderate'), ('Low', 'low')], default='Moderate', max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.location')),
            ],
        ),
        migrations.CreateModel(
            name='Incidence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incidence_type', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('time_of_incident', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('resolved', 'Resolved'), ('cancelled', 'Cancelled')], default='pending', max_length=50)),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.calls')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.location')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.incidence')),
                ('responders', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]