# Generated by Django 2.2 on 2021-05-06 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0005_auto_20210505_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='products',
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='online_shop.Product'),
        ),
    ]
