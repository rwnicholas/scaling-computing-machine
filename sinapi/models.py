from django.db import models


# Create your models here.
class Material(models.Model):
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=255)
    unidade = models.CharField(max_length=5)

    class Meta:
        app_label = 'sinapi'

class Material_Historico_Precos(models.Model):
    idMaterial = models.ForeignKey(
        Material, on_delete=models.CASCADE
    )
    preco = models.FloatField()
    data = models.DateField()

    class Meta:
        app_label = 'sinapi'
        unique_together = ('idMaterial', 'preco')