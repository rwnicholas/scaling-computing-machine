from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.IntegerField(name='id', primary_key=True)
    description = models.CharField(name='description', max_length=500)
    price = models.DecimalField(name='price', max_digits=8, decimal_places=2)
    brand = models.CharField(name='brand',max_length=100, default="")
    storeName = models.CharField(name='storeName', max_length=100)
    notes = models.CharField(name='notes', max_length=100)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.description

class ProductsPrices(models.Model):
    """
    Classe responsável pelo armazenamento dos preços antigos de um produto x.
    """
    product = models.ForeignKey(Product,on_delete=models.CASCADE,)
    untilDate = models.DateField(name='untilDate', auto_now=True)
    price = models.DecimalField(name='price', max_digits=8, decimal_places=2)

    def __str__(self):
        return f'Produto: {self.product.id} atualizado na data {self.untilDate} com o preço de R${self.price}'