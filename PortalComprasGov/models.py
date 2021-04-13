from django.db import models

# Create your models here.
class GrupoMaterial(models.Model):
    codigo = models.IntegerField(unique=True)
    descricao = models.CharField(max_length=255)

class Material(models.Model):
    idGrupo = models.ForeignKey(
        GrupoMaterial, on_delete=models.CASCADE
    )
    descricao = models.CharField(max_length=255, unique=True)
    licitacao = models.CharField(max_length=255)
    unidade = models.CharField(max_length=255)

    class Meta:
        app_label = "PortalComprasGov"


class Material_Historico_Precos(models.Model):
    idMaterial = models.ForeignKey(
        Material, on_delete=models.CASCADE
    )
    preco = models.FloatField()
    data = models.DateField()

    class Meta:
        app_label = "PortalComprasGov"
        unique_together = ('idMaterial', 'preco')

