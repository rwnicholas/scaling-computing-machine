# Este arquivo eh responsavel pela serializacao dos models, ou seja, pela conversao para JSON ou de JSON para o modelo

from rest_framework import serializers
from .models import Product, ProductsPrices

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','description', 'price', 'brand', 'storeName','notes')

class ProductsPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsPrices
        fields = ('product','untilDate','price')