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
    sinapiDict = {}
    ecoalDict = {}
    comprasGovDict = {}

    ecoalMateriais = EcoAL.models.Material.objects.filter(nome__istartswith=searchTerm)
    sinapiMateriais = sinapi.models.Material.objects.filter(nome__istartswith=searchTerm)
    comprasGovMateriais = PortalComprasGov.models.Material.objects.filter(descricao__istartswith=searchTerm)

    #### SINAPI
    if sinapiCheck:
        for material in sinapiMateriais:
            sinapiDict[material.nome] = sinapi.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-data')[:1].values()
            sinapiDict[material.nome] = sinapiDict[material.nome][0]
            sinapiDict[material.nome]  = [sinapiDict[material.nome], material.unidade]
    OutputDict['SINAPI'] = sinapiDict

    #### Economiza Alagoas
    if ecoalCheck:
        for material in ecoalMateriais:
            ecoalDict[material.nome] = EcoAL.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-data')[:1].values()
            ecoalDict[material.nome] = ecoalDict[material.nome][0]
    OutputDict['ecoAL'] = ecoalDict
    
    ### Portal de Compras Governamentais
    if portalGovCheck:
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

        returnedData.pop('countSinapi', None)
        returnedData.pop('countEcoAL', None)
        returnedData.pop('countComprasGov', None)

        return Response(data=returnedData,status=status.HTTP_200_OK)
 
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)