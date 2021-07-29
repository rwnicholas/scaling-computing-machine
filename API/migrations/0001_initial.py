# Generated by Django 3.1.5 on 2021-01-12 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.CharField(max_length=500)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
