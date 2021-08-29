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
        base.data = pd.DataFrame(list(sinapi_Material.objects.all().values('cod', 'description')))
        base.generalizeString(column='description')
        knn = KNN('classifier/train_NCM.csv', 6)

        #codSinapi, ncm, description, price
        for row in base.data.iterrows():
            termo = row[1]['description']
            r = RequestSEFAZ()
            ecoData = r.request(term=termo)

            for dictionary in ecoData.json():
                if (knn.classifier(int(dictionary['codNcm'])) == "MATERIAIS DE CONSTRUCAO"):
                    try:
                        newMaterial,created = Material.objects.get_or_create(
                            codSinapi=row[1]['cod'],
                            codGetin=dictionary['codGetin'],
                            ncm=dictionary['codNcm'],
                            description=dictionary['dscProduto']
                        )
                    except IntegrityError: continue
                    except:
                        return False
                    
                    try:
                        newMaterialPreco = Material_Historico_Precos(
                            idMaterial=newMaterial,
                            price=dictionary['valUnitarioUltimaVenda']
                        )

                        newMaterialPreco.save()
                    except IntegrityError: continue
                    except:
                        return False
        return True
    except:
        return False
