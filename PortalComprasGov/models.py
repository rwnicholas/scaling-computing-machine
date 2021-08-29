from django.db import models

# Create your models here.
class GrupoMaterial(models.Model):
    cod = models.IntegerField(unique=True)
    description = models.CharField(max_length=255)

class Material(models.Model):
    idGrupo = models.ForeignKey(
        GrupoMaterial, on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255, unique=True)
    bidding = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

    class Meta:
        app_label = "PortalComprasGov"


class Material_Historico_Precos(models.Model):
    idMaterial = models.ForeignKey(
        Material, on_delete=models.CASCADE
    )
    price = models.FloatField()
    date = models.DateField()

    class Meta:
        app_label = "PortalComprasGov"
        unique_together = ('idMaterial', 'price')

