"""SEFAZ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import sinapi.views as urlSinapi
import EcoAL.views as urlEcoAL
import PortalComprasGov.views as urlPortalComprasGov
import AquiSeFaz.views as url
import web.views as urlCommercialPrices


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('sinapi/', urlSinapi.sinapi, name='sinapi'),
    # path('ecoal/', urlEcoAL.ecoal, name='ecoal'),
    # path('portalCompras/', urlPortalComprasGov.portalCompras, name='portalComprasGov'),
    path('', url.selectBase, name='searchPrice'),
    path('retriveAPIs/', url.retriveAPIs, name='retrieveInfoFromAPIs'),
    # path('novoTema/', url.index, name='novoTema'),
    path('search.json', url.searchPriceAPI, name='searchPriceAPI'),
    path('commercialPrices/', urlCommercialPrices.index, name='commercialPrices'),
    path('api/', include('API.urls'))
]
