# Generated by Django 3.2.8 on 2021-10-24 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recomendations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=50)),
                ('req_1', models.CharField(max_length=50)),
                ('req_2', models.CharField(max_length=50)),
                ('req_3', models.CharField(max_length=50)),
                ('req_4', models.CharField(max_length=50)),
                ('req_5', models.CharField(max_length=50)),
            ],
        ),
    ]