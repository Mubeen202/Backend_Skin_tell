# Generated by Django 4.2.10 on 2024-02-27 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='predictions_images'),
        ),
    ]
