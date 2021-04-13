#!/usr/bin/python3
from Request import RequestGet

def navigatePages(url, params):
	objeto = RequestGet(params, url)
	QTD_JANELA_EXIBICAO = 500
	offset = 0
	pagesOf = []
	pagesOf.append(objeto.returnedData)

	while objeto.count >= QTD_JANELA_EXIBICAO:
		objeto.count -= QTD_JANELA_EXIBICAO
		offset+=QTD_JANELA_EXIBICAO
		params['offset'] = offset
		objeto.request(params, url)
		pagesOf.append(objeto.returnedData)

	return pagesOf
		
def main():
	#Materiais
	pagesMateriais = navigatePages("http://compras.dados.gov.br/materiais/v1/materiais.json", 
		{
			"grupo":56
		}
	)
	codigoMateriais = []
	for page in pagesMateriais:
		materiais = page['_embedded']
		materiais = list(materiais.values())
		for material in materiais[0]:
			#Material_Codigo
			codigoMateriais.append(material['codigo'])
	
	#Licitações
	for codigo in codigoMateriais:
		pagesLicitacoes = navigatePages("http://compras.dados.gov.br/licitacoes/v1/licitacoes.json",
			    {
			        "item_material": codigo,
					"data_publicacao_min": "2015-01-01"
			    }
		)
		codigoLicitacoes = []
		for page in pagesLicitacoes:
			licitacoes = page['_embedded']
			licitacoes = list(licitacoes.values())

			# A API retorna licitações duplicadas
			for licitacao in licitacoes[0]:

				itensPages = navigatePages("http://compras.dados.gov.br/licitacoes/doc/licitacao/" + licitacao['identificador'] + "/itens.json",
						{}
				)

				for pageItem in itensPages:
					itens = pageItem['_embedded']
					itens = list(itens.values())
					for item in itens[0]:
						if codigo == item['codigo_item_material']:
							print(licitacao['identificador'], ": ", item['descricao_item'])


main()
