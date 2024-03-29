# Generated by Django 3.2.6 on 2021-09-03 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20210902_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=256)),
                ('receiver', models.CharField(max_length=256)),
                ('messages', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='usid',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
