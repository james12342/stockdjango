# Generated by Django 2.2.15 on 2022-05-18 06:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_ads_postadmaxearn'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='adPostBy',
            field=models.CharField(choices=[('Superuser', 'Superuser'), ('Author', 'Author')], default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
