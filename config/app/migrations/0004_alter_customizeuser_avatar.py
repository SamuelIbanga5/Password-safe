# Generated by Django 4.0.1 on 2022-04-15 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_customizeuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customizeuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/'),
        ),
    ]
