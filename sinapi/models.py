from django.db import models


# Create your models here.
class Material(models.Model):
    cod = models.IntegerField(unique=True)
    description = models.CharField(max_length=255)
    unit = models.CharField(max_length=5)

    class Meta:
        app_label = 'sinapi'

class Material_Historico_Precos(models.Model):
    idMaterial = models.ForeignKey(
        Material, on_delete=models.CASCADE
    )
    price = models.FloatField()
    date = models.DateField()

    class Meta:
        app_label = 'sinapi'
        unique_together = ('idMaterial', 'price')