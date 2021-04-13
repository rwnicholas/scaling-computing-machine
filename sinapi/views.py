from django.shortcuts import render,redirect,reverse
from django.templatetags.static import static
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .models import Material,Material_Historico_Precos
from AquiSeFaz.views import index
import classifier.NCM
# Create your views here.

def sinapi(request):
    data = classifier.NCM.returnCleanData('static/baseOld.xls', 'static/baseNew.xls')
    context = {
        'status': True
    }
    for row in data.iterrows():
        row[1]['PRECO MEDIANO R$'] = row[1]['PRECO MEDIANO R$'].replace('.', '')
        row[1]['PRECO MEDIANO R$'] = row[1]['PRECO MEDIANO R$'].replace(',', '.')
        try:
            newMaterial,created = Material.objects.get_or_create(
                codigo=row[1]['CODIGO'],
                nome=row[1]['DESCRICAO DO INSUMO'],
                unidade=row[1]['UNIDADE']
            )
        except IntegrityError: continue
        
        newPrecoMaterial = Material_Historico_Precos(
            idMaterial=newMaterial, preco=row[1]['PRECO MEDIANO R$'],
            data=row[1]['DATA']
        )
        try:
            newPrecoMaterial.save()
        except IntegrityError: continue
        except:
            context['status'] = False
            break

    return index(request, context)