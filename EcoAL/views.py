from django.shortcuts import render
from sinapi.models import Material as sinapi_Material
from .models import Material,Material_Historico_Precos
from classifier.NCM import NCM
from classifier.Request import RequestSEFAZ
from classifier.KNN import KNN
from django.db import IntegrityError
from AquiSeFaz.views import retriveAPIs
import pandas as pd

# Create your views here.

def ecoal():
    try:
        print("Atualizando Economiza Alagoas")
        base = NCM(None)
        base.data = pd.DataFrame(list(sinapi_Material.objects.all().values('codigo', 'nome')))
        base.generalizeString(column='nome')
        knn = KNN('classifier/train_NCM.csv', 6)

        #codigoSinapi, ncm, nome, preco
        for row in base.data.iterrows():
            termo = row[1]['nome']
            r = RequestSEFAZ()
            ecoData = r.request(term=termo)

            for dictionary in ecoData.json():
                if (knn.classifier(int(dictionary['codNcm'])) == "MATERIAIS DE CONSTRUCAO"):
                    try:
                        newMaterial,created = Material.objects.get_or_create(
                            codigoSinapi=row[1]['codigo'],
                            codGetin=dictionary['codGetin'],
                            ncm=dictionary['codNcm'],
                            nome=dictionary['dscProduto']
                        )
                    except IntegrityError: continue
                    except:
                        return False
                    
                    try:
                        newMaterialPreco = Material_Historico_Precos(
                            idMaterial=newMaterial,
                            preco=dictionary['valUnitarioUltimaVenda']
                        )

                        newMaterialPreco.save()
                    except IntegrityError: continue
                    except:
                        return False
        return True
    except:
        return False
