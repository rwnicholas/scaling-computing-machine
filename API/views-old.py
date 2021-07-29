from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action

from .serializers import ProductSerializer
from .models import Product

# O tipo ModelViewSet eh uma classe especial que vai intermediar os metodos GET e POST para os produtos
class ProductViewSet(viewsets.ModelViewSet):
    search_fields = ['description','storeName', 'brand'] #dizendo que se pode procurar os itens pela descricao e pelo nome da loja
    filter_backends = (filters.SearchFilter,)
    queryset = Product.objects.all().order_by('description')
    serializer_class = ProductSerializer
    print("view")

    
