# Generated by Django 4.1.3 on 2022-11-17 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('dateopen', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('lic', models.BigIntegerField()),
                ('contact', models.BigIntegerField()),
                ('email', models.EmailField(max_length=50, null=True)),
                ('rating', models.IntegerField(null=True)),
                ('realrat', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=50)),
                ('contact', models.BigIntegerField()),
                ('password', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=200)),
                ('dateofreview', models.DateField(auto_now_add=True)),
                ('hotelname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewapp.hotels')),
                ('uname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewapp.registration')),
            ],
        ),
    ]