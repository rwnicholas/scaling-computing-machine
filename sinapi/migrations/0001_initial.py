# Generated by Django 3.2.6 on 2021-08-29 16:06

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
                ('cod', models.IntegerField(unique=True)),
                ('description', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Material_Historico_Precos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('date', models.DateField()),
                ('idMaterial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sinapi.material')),
            ],
            options={
                'unique_together': {('idMaterial', 'price')},
            },
        ),
    ]
