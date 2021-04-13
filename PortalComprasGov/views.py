from django.shortcuts import render
from classifier.Request import RequestGet
from AquiSeFaz.views import index
from .models import Material, Material_Historico_Precos, GrupoMaterial
from django.db import IntegrityError
from datetime import datetime
# Create your views here.

def navigatePages(url, params):
	objeto = RequestGet(params, url)
	QTD_JANELA_EXIBICAO = 500
	offset = 0
	pagesOf = []
	pagesOf.append(objeto.returnedData)

	while objeto.count > QTD_JANELA_EXIBICAO:
		objeto.count -= QTD_JANELA_EXIBICAO
		offset+=QTD_JANELA_EXIBICAO
		params['offset'] = offset
		objeto.request(params, url)
		pagesOf.append(objeto.returnedData)

	return pagesOf
		
def portalCompras(request):
	context = {
			'status': True
	}
	#Materiais
	print("Requisição Materiais")
	pagesMateriais = navigatePages("http://compras.dados.gov.br/materiais/v1/materiais.json", 
		{
			"grupo":56
		}
	)
	print("Lista de materiais - OK\n")
	codigoMateriais = []
	for page in pagesMateriais:
		materiais = page['_embedded']
		materiais = list(materiais.values())
		for material in materiais[0]:
			#Material_Codigo
			codigoMateriais.append((material['codigo'], material['descricao']))
	
	licitacoesDescartadas = []

	#Licitações
	for codigo,descricaoMaterial in codigoMateriais:
		pagesLicitacoes = navigatePages("http://compras.dados.gov.br/licitacoes/v1/licitacoes.json",
				{
					"item_material": codigo,
					"data_publicacao_min": "2019-01-01"
				}
		)

		for page in pagesLicitacoes:
			licitacoes = page['_embedded']
			licitacoes = list(licitacoes.values())
			
			# A API retorna licitações duplicadas
			for licitacao in licitacoes[0]:
				if licitacao['identificador'] in licitacoesDescartadas:
					continue
				

				itensPages = navigatePages("http://compras.dados.gov.br/licitacoes/doc/licitacao/" + licitacao['identificador'] + "/itens.json",
						{}
				)

				print(licitacao['identificador'])
				
				for cod,DescMat in codigoMateriais:
					for pageItem in itensPages:

						print("Started page at:", datetime.now())
						itens = pageItem['_embedded']
						itens = list(itens.values())

						for item in itens[0]:
							if cod == item['codigo_item_material'] and (item['valor_estimado'] != None and item['valor_estimado'] > 0):
								print(item['numero_licitacao'], item['codigo_item_material'], DescMat, (float(item['valor_estimado'])/float(item['quantidade'])))
								try:
									newGrupo,created = GrupoMaterial.objects.get_or_create(
										codigo=item['codigo_item_material'],
										descricao=DescMat,
									)
								except IntegrityError: continue
								except:
									context['status'] = False
									break

								try:
									newMaterial,created = Material.objects.get_or_create(
										idGrupo=newGrupo,
										descricao=item['descricao_item'],
										licitacao=item['numero_licitacao'],
										unidade=item['unidade']
									)
								except IntegrityError: continue
								except:
									context['status'] = False
									break
								
								try:
									newPrecoMaterial = Material_Historico_Precos(
										idMaterial=newMaterial,
										preco=(float(item['valor_estimado'])/float(item['quantidade'])),
										data=licitacao['data_publicacao']
									)
									newPrecoMaterial.save()
								except IntegrityError: continue
								except:
									context['status'] = False
									break
						print("Finished page at:", datetime.now())
				licitacoesDescartadas.append(licitacao['identificador'])
	return index(request, context)