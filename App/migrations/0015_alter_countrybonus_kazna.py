# Generated by Django 3.2.5 on 2021-08-17 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0014_alter_countrybonus_kazna'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrybonus',
            name='kazna',
            field=models.IntegerField(default=10000000),
        ),
    ]