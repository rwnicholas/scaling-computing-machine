from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, ProductsPrices
from .serializers import ProductSerializer, ProductsPricesSerializer

class ProductAPIView(APIView):
    """
    API dos Produtos
    """
    def get(self,request,pk=None):
        if(pk!=None):
            product = Product.objects.filter(id=pk)
            if(not product.exists()):
                data = {'has-product': False}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ProductSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def put(self,request,pk):
        product = Product.objects.get(id=pk)

        # criar uma instancia no versionamento de periodos
        productPrice = ProductsPrices()
        productPrice.product = product
        productPrice.price = product.price
        productPrice.save()

        # atualizar produto
        data = request.data

        if("price" in data.keys()):
            product.price = data["price"]

        if("description" in data.keys()):
            product.description = data["description"]
        if("storeName" in data.keys()):
            product.storeName = data["storeName"]
        if("notes" in data.keys()):
            product.notes = data["notes"]
        if("brand" in data.keys()):
            product.brand = data["brand"]

        product.save()
        return Response(status=status.HTTP_200_OK)

class ProductsPricesAPIView(APIView):
    """
    API dos períodos de atualização dos produtos.
    """
    def get(self,request,pk=None):
        if(pk!=None):
            periods = ProductsPrices.objects.filter(product_id=pk)
            print("periods: ", periods)
            serializer = ProductsPricesSerializer(periods,many=True)
            return Response(serializer.data)

        periods = ProductsPrices.objects.all()
        serializer = ProductsPricesSerializer(periods,many=True)
        return Response(serializer.data)