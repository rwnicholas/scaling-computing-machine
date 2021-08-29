from typing import Tuple
from django.shortcuts import render,redirect,reverse
from django.templatetags.static import static
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .models import Material,Material_Historico_Precos
from AquiSeFaz.views import retriveAPIs
import classifier.NCM
# Create your views here.

def sinapi():
    try:
        print("Atualizando Sinapi")
        data = classifier.NCM.returnCleanData('static/baseOld.xls', 'static/baseNew.xls')
        
        for row in data.iterrows():
            row[1]['PRECO MEDIANO R$'] = row[1]['PRECO MEDIANO R$'].replace('.', '')
            row[1]['PRECO MEDIANO R$'] = row[1]['PRECO MEDIANO R$'].replace(',', '.')
            try:
                newMaterial,created = Material.objects.get_or_create(
                    cod=row[1]['CODIGO'],
                    description=row[1]['DESCRICAO DO INSUMO'],
                    unit=row[1]['UNIDADE']
                )
            except IntegrityError: continue
            
            newPrecoMaterial = Material_Historico_Precos(
                idMaterial=newMaterial, price=row[1]['PRECO MEDIANO R$'],
                date=row[1]['DATA']
            )
            try:
                newPrecoMaterial.save()
            except IntegrityError: continue
            except:
                return False

        return True
    except:
        return False