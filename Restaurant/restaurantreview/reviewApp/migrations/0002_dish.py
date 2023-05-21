# Generated by Django 4.1.3 on 2022-11-17 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviewapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishname', models.CharField(max_length=20)),
                ('hotelname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewapp.hotels')),
            ],
        ),
    ]