# Generated by Django 3.1.5 on 2021-01-27 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkshopu', '0010_product_origin_product_size_selected_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selected_Product_Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.PositiveIntegerField()),
                ('product_pic', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]