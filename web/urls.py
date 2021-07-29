from django.urls import path, re_path

from .views import index,root

urlpatterns = [
    path('commercialPrices/', index, name='commercialPrices'), #observacao: aqui eh "" pq na url do projeto ja indica o web/
    path('', root,name='root')
]