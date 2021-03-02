from django.core.paginator import Paginator
from django.shortcuts import render
from itertools import chain
import EcoAL.models
import sinapi.models
import PortalComprasGov.models

# Create your views here.

def index(request, context = {}):
    return render(request, 'index.html', context=context)

def searchPrice(request):
    context = {}
    sinapiDict = {}
    ecoalDict = {}
    comprasGovDict = {}

    if 'searchTerm' in request.GET:
        if request.GET['searchTerm'] == None or request.GET['searchTerm'] == '':
            print("Seligarapa")

        ecoalMateriais = EcoAL.models.Material.objects.filter(nome__istartswith=request.GET['searchTerm'])
        sinapiMateriais = sinapi.models.Material.objects.filter(nome__istartswith=request.GET['searchTerm'])
        comprasGovMateriais = PortalComprasGov.models.Material.objects.filter(descricao__istartswith=request.GET['searchTerm'])
        
        context['products'] = []

        #### SINAPI
        
        for material in sinapiMateriais:
            sinapiDict[material.nome] = sinapi.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-data')[:1]
        context['SINAPI'] = sinapiDict

        #### Economiza Alagoas
        
        for material in ecoalMateriais:
            ecoalDict[material.nome] = EcoAL.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-data')[:1]
        context['ecoAL'] = ecoalDict
        
        ### Portal de Compras Governamentais
        
        for material in comprasGovMateriais:
            comprasGovDict[material.descricao] = PortalComprasGov.models.Material_Historico_Precos.objects.filter(idMaterial=material.id).order_by('-data')[:1]
        context['comprasGov'] = comprasGovDict

        if (len(context['SINAPI']) == 0) and (len(context['ecoAL']) == 0) and (len(context['comprasGov']) == 0):
            context['status'] = False
            print("SorryMan")
        else:
            context['countSinapi'] = len(context['SINAPI'])
            context['countEcoAL'] = len(context['ecoAL'])
            context['countComprasGov'] = len(context['comprasGov'])
    
    # itens = chain(sinapiDict, ecoalDict, comprasGovDict)
    # print(itens)
    # paginator = Paginator(list(itens), 25)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'searchPrice.html', context)