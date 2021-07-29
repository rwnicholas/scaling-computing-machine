from django.urls import path, include

from .views import ProductAPIView, ProductsPricesAPIView

urlpatterns = [
    path('', ProductAPIView.as_view(), name='products'),
    path('<int:pk>/', ProductAPIView.as_view(), name='products'),
    path('<int:pk>/periods/', ProductsPricesAPIView.as_view(), name='products_prices'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]