from django.db import models

# Create your models here.
class Material(models.Model):
    codigoSinapi = models.IntegerField()
    codGetin = models.CharField(max_length=255)
    ncm = models.CharField(max_length=255)
    nome = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'EcoAL'

class Material_Historico_Precos(models.Model):
    idMaterial = models.ForeignKey(
        Material, on_delete=models.CASCADE
    )
    preco = models.FloatField()
    data = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('idMaterial', 'preco')
        app_label = 'EcoAL'