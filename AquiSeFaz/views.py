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

# Create your views here.

def retriveAPIs(request, context = {}):
    return render(request, 'retrieveInfoFromAPIs.html', context=context)

def index(request):
    return render(request, 'index.html')

def searchPriceBase(searchTerm, ecoalCheck = True, portalGovCheck = True, sinapiCheck = True):
    OutputDict = {}
    OutputDict['produtos'] = []

    ecoalMateriais = EcoAL.models.Material.objects.filter(description__istartswith=searchTerm)
    sinapiMateriais = sinapi.models.Material.objects.filter(description__istartswith=searchTerm)
    comprasGovMateriais = PortalComprasGov.models.Material.objects.filter(description__istartswith=searchTerm)

    #### SINAPI
    if sinapiCheck:
        for material in sinapiMateriais:
            queryset = sinapi.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-date')[:1].values()[0]
            queryset
            OutputDict['produtos'].append((material, queryset))

    #### Economiza Alagoas
    if ecoalCheck:
        for material in ecoalMateriais:
            queryset = EcoAL.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-date')[:1].values()[0]
            OutputDict['produtos'].append((material, queryset))
    
    ### Portal de Compras Governamentais
    if portalGovCheck:
        for material in comprasGovMateriais:
            queryset = PortalComprasGov.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-date')[:1].values()[0]
            OutputDict['produtos'].append((material, queryset))
    
    return OutputDict

def selectBase(request):
    context = {}
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
            context.update(searchPriceGov(request.GET['searchTerm'], ecoalCheck, portalGovCheck, sinapiCheck))
        
        if carajasCheck or leroyCheck or tupanCheck:
            context.update(getProductsInfo(request.GET['searchTerm'], carajasCheck, leroyCheck, tupanCheck))

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