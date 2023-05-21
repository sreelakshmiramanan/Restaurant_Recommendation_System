# Generated by Django 4.1.4 on 2023-04-27 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviewapp', '0004_dish_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.CharField(max_length=20)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reviewapp.hotels')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewapp.registration')),
            ],
        ),
    ]