# Generated by Django 3.1.3 on 2021-02-25 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoSinapi', models.IntegerField()),
                ('codGetin', models.CharField(max_length=255)),
                ('ncm', models.CharField(max_length=255)),
                ('nome', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material_Historico_Precos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.FloatField()),
                ('data', models.DateField(auto_now_add=True)),
                ('idMaterial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EcoAL.material')),
            ],
            options={
                'unique_together': {('idMaterial', 'preco')},
            },
        ),
    ]
