# Generated by Django 4.2.4 on 2024-06-04 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0002_alter_incidence_call'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidence',
            name='call',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.calls'),
        ),
    ]