# Generated by Django 2.2 on 2021-05-09 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0008_auto_20210508_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='star',
            field=models.IntegerField(null=True),
        ),
    ]
