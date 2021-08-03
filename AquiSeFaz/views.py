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
import json

# Create your views here.

def retriveAPIs(request, context = {}):
    return render(request, 'retrieveInfoFromAPIs.html', context=context)

def index(request):
    return render(request, 'index.html')

def searchPriceBase(searchTerm):
    OutputDict = {}
    sinapiDict = {}
    ecoalDict = {}
    comprasGovDict = {}

    ecoalMateriais = EcoAL.models.Material.objects.filter(nome__istartswith=searchTerm)
    sinapiMateriais = sinapi.models.Material.objects.filter(nome__istartswith=searchTerm)
    comprasGovMateriais = PortalComprasGov.models.Material.objects.filter(descricao__istartswith=searchTerm)

    #### SINAPI
    
    for material in sinapiMateriais:
        sinapiDict[material.nome] = sinapi.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-data')[:1].values()
        sinapiDict[material.nome] = sinapiDict[material.nome][0]
        sinapiDict[material.nome]  = [sinapiDict[material.nome], material.unidade]
    OutputDict['SINAPI'] = sinapiDict

    #### Economiza Alagoas
    
    for material in ecoalMateriais:
        ecoalDict[material.nome] = EcoAL.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-data')[:1].values()
        ecoalDict[material.nome] = ecoalDict[material.nome][0]
    OutputDict['ecoAL'] = ecoalDict
    
    ### Portal de Compras Governamentais
    
    for material in comprasGovMateriais:
        comprasGovDict[material.descricao] = PortalComprasGov.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-data')[:1].values()
        comprasGovDict[material.descricao] = comprasGovDict[material.descricao][0]
        comprasGovDict[material.descricao] = [comprasGovDict[material.descricao], material.unidade]
    OutputDict['comprasGov'] = comprasGovDict

    if (len(OutputDict['SINAPI']) == 0) and (len(OutputDict['ecoAL']) == 0) and (len(OutputDict['comprasGov']) == 0):
        OutputDict['status'] = False
        print("SorryMan")
    else:
        OutputDict['countSinapi'] = len(OutputDict['SINAPI'])
        OutputDict['countEcoAL'] = len(OutputDict['ecoAL'])
        OutputDict['countComprasGov'] = len(OutputDict['comprasGov'])
    
    return OutputDict

def searchPrice(request):
    context = {}
    if 'searchTerm' in request.GET:
        if request.GET['searchTerm'] == None or request.GET['searchTerm'] == '':
            print("Seligarapa")

        context = searchPriceBase(request.GET['searchTerm'])

    return render(request, 'searchPrice.html', context)

@api_view(['GET'])
def searchPriceAPI(request):
    if 'searchTerm' in request.GET and request.GET['searchTerm'] != None and request.GET['searchTerm'].strip() != '':
        returnedData = searchPriceBase(request.GET['searchTerm'])

        returnedData.pop('countSinapi', None)
        returnedData.pop('countEcoAL', None)
        returnedData.pop('countComprasGov', None)

        return Response(data=returnedData,status=status.HTTP_200_OK)
 
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)