from django.db import models

# Create your models here.
class Material(models.Model):
    codSinapi = models.IntegerField()
    codGetin = models.CharField(max_length=255)
    ncm = models.CharField(max_length=255)
    description = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'EcoAL'

class Material_Historico_Precos(models.Model):
    idMaterial = models.ForeignKey(
        Material, on_delete=models.CASCADE
    )
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('idMaterial', 'price')
        app_label = 'EcoAL'