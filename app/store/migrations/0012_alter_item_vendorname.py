# Generated by Django 4.0.2 on 2022-03-19 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_item_vendorname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='vendorName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.vendordetail'),
        ),
    ]
