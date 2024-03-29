# Generated by Django 2.2.24 on 2021-10-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_midroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='midroom',
            name='second_person',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='friends',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='midroom',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usid',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
