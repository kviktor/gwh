# Generated by Django 3.1.7 on 2021-03-14 11:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetricConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('token', models.UUIDField(default=uuid.uuid4)),
                ('prefix', models.CharField(blank=True, default='', help_text='add this prefix to the metric path', max_length=64)),
                ('carbon_host', models.CharField(help_text='used for the socket connection', max_length=64)),
                ('carbon_port', models.PositiveIntegerField(help_text='used for the socket connection')),
            ],
        ),
    ]