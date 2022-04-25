# Generated by Django 3.2.13 on 2022-04-24 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=44)),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='product_images/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
