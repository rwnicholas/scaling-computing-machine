# from django.core.paginator import Paginator
from django.shortcuts import render
from itertools import chain
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import EcoAL.models
import sinapi.models
import PortalComprasGov.models
from web.views import getProductsInfo
from django.core.paginator import Paginator

# Create your views here.

def retriveAPIs(request, context = {}):
    return render(request, 'retrieveInfoFromAPIs.html', context=context)

def index(request):
    return render(request, 'index.html')

def searchPriceBase(searchTerm, ecoalCheck = True, portalGovCheck = True, sinapiCheck = True):
    products = []


    #### SINAPI
    if sinapiCheck:
        sinapiMateriais = sinapi.models.Material.objects.filter(description__istartswith=searchTerm)
        for material in sinapiMateriais:
            queryset = sinapi.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-date')[:1].values()
            material.storeName = "SINAPI"
            products.append((material, queryset[0]))

    #### Economiza Alagoas
    if ecoalCheck:
        ecoalMateriais = EcoAL.models.Material.objects.filter(description__istartswith=searchTerm)
        for material in ecoalMateriais:
            queryset = EcoAL.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-date')[:1].values()
            material.storeName = "Economiza Alagoas"
            products.append((material, queryset[0]))
    
    ### Portal de Compras Governamentais
    if portalGovCheck:
        comprasGovMateriais = PortalComprasGov.models.Material.objects.filter(description__istartswith=searchTerm)
        for material in comprasGovMateriais:
            queryset = PortalComprasGov.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-date')[:1].values()
            material.storeName = "Portal de Compras Governamentais"
            products.append((material, queryset[0]))
    
    return products

def selectBase(request, context = {}):
    products = []

    if 'searchTerm' in request.GET:
        if request.GET['searchTerm'] == None or request.GET['searchTerm'] == '':
            raise ValueError

        basesList = request.GET.getlist('bases')

        ecoalCheck = True if 'ecoal' in basesList else False
        portalGovCheck = True if 'portalGov' in basesList else False
        sinapiCheck = True if 'sinapi' in basesList else False
        carajasCheck = True if 'carajas' in basesList else False
        leroyCheck = True if 'leroy' in basesList else False
        tupanCheck = True if 'tupan' in basesList else False

        # ecoal, sinapi, portalGov, carajas, leroy, tupan
        
        if ecoalCheck or portalGovCheck or sinapiCheck:
            products+= searchPriceGov(request.GET['searchTerm'], ecoalCheck, portalGovCheck, sinapiCheck)
        
        if carajasCheck or leroyCheck or tupanCheck:
            products+= getProductsInfo(request.GET['searchTerm'], carajasCheck, leroyCheck, tupanCheck)

        paginator = Paginator(products, 10)
        page_number = request.GET.get('page', 1)
        context['products'] = paginator.get_page(page_number)

        queries_without_page = request.GET.copy()
        if 'page' in queries_without_page:
            del queries_without_page['page']

        context['queries'] = queries_without_page

    return render(request, 'searchPrice.html', context)

def searchPriceGov(searchTerm, ecoalCheck, portalGovCheck, sinapiCheck):
    return searchPriceBase(searchTerm, ecoalCheck, portalGovCheck, sinapiCheck)

@api_view(['GET'])
def searchPriceAPI(request):
    if 'searchTerm' in request.GET and request.GET['searchTerm'] != None and request.GET['searchTerm'].strip() != '':
        returnedData = searchPriceBase(request.GET['searchTerm'])

        return Response(data=returnedData,status=status.HTTP_200_OK)
 
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)