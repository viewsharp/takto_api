# Generated by Django 3.1.3 on 2020-11-07 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20201107_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='hours',
            field=models.JSONField(null=True),
        ),
    ]
