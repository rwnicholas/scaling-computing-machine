#!/usr/bin/python3
import pandas as pd
import re
import os
from datetime import datetime

class NCM:
	data = None
	
	def __init__(self, fileName, date=None):
		if fileName == None: return
		trash = pd.read_excel(fileName)
		self.data = trash[6:-2]
		self.data = self.data.rename(columns={'        PRECOS DE INSUMOS': 'CODIGO',
											'Unnamed: 1': 'DESCRICAO DO INSUMO',
											'Unnamed: 2': 'UNIDADE',
											'Unnamed: 3': 'ORIGEM DO PRECO',
											'Unnamed: 4': 'PRECO MEDIANO R$'
											})
		self.data['DATA'] = date

	def info(self):
		return self.data.head()

	def split(self):
		self.data["ncm"] = self.data["ncm"].str.split("|")
		self.data = self.data.apply(pd.Series.explode)

		self.data["ncm"] = self.data["ncm"].str.replace('.', '')
		self.data = self.data.sort_values('ncm', ascending=False)
		self.data.drop_duplicates(subset="ncm", keep='first', inplace=True)
		self.data = self.data.reset_index()
		self.data = self.data.drop("index", axis=1)
		self.data = self.data.drop("not_ncm", axis=1)

		return self.data

	def save(self, savingName):
		self.data.to_csv(savingName, index=False)

	def generalizeString(self, column='DESCRICAO DO INSUMO'):
		self.data[column] = self.data[column].apply(lambda x: self.keepOnlyAlhpa(x))
		self.data = self.data.sort_values(column, ascending=False)
		self.data.drop_duplicates(subset=column, keep='first', inplace=True)
		self.data = self.data.reset_index()
		self.data = self.data.drop("index", axis=1)
	
	def removeSpaces(self):
		self.data['DESCRICAO DO INSUMO'] = self.data['DESCRICAO DO INSUMO'].apply(lambda x: re.sub('\s{2,}', ' ', x))
		self.data['DESCRICAO DO INSUMO'] = self.data['DESCRICAO DO INSUMO'].apply(lambda x: x.replace("!EM PROCESSO DESATIVACAO!", ""))
		self.data['DESCRICAO DO INSUMO'] = self.data['DESCRICAO DO INSUMO'].apply(lambda x: x.replace("!EM PROCESSO DE DESATIVACAO!", ""))
		self.data['DESCRICAO DO INSUMO'] = self.data['DESCRICAO DO INSUMO'].apply(lambda x: x.strip())
		self.data['UNIDADE'] = self.data['UNIDADE'].apply(lambda x: re.sub('\s{2,}', ' ', x))
		self.data['ORIGEM DO PRECO'] = self.data['ORIGEM DO PRECO'].apply(lambda x: re.sub('\s{2,}', ' ', x))
		self.data['PRECO MEDIANO R$'] = self.data['PRECO MEDIANO R$'].apply(lambda x: re.sub('\s{2,}', ' ', x))

	def limitSizeRemovingWord(self, string):
		MAX_LENGHT = 30
		if len(string) > MAX_LENGHT:
			work_string = string[:MAX_LENGHT+1]
			if work_string[MAX_LENGHT].isalpha():
				for i in range(MAX_LENGHT, -1, -1):
					if work_string[i].isalpha():
						continue
					else:
						new_string = work_string[:i+1]
						break
			else:
				new_string = work_string
		else:
			new_string = string

		return new_string

	def limitTwoWords(self, string):
		countSpaces = 0
		QTD_WORDS = 2
		for i in range(len(string)):
			if string[i] == ' ':
				countSpaces+=1
			if countSpaces == QTD_WORDS:
				return string[:i]
		return string

	def keepOnlyAlhpa(self, text):
		output = list([val for val in text
						if val.isalpha() or val == " "])
		output = "".join(output)
		
		output = output.replace("EM PROCESSO DE DESATIVACAO", "")
		output = output.replace("EM PROCESSO DESATIVACAO", "")
		output = output.replace("MM", "")
		output = output.replace("CM", "")
		output = output.replace("  X", "")
		output = output.replace("M X M", "")
		output = output.replace("LARGURA", "")
		output = output.replace(" FUROS XX", "")
		output = output.replace(" PARA ", " ")
		output = output.replace(" DE ", " ")
		output = output.replace(" EM ", " ")
		output = output.replace(" OU ", " ")
		output = output.replace(" COM ", " ")
		output = output.replace(" A ", " ")
		output = output.rstrip()
		output = output.lstrip()
		output = re.sub('\s{2,}', ' ', output)
		output = self.limitSizeRemovingWord(output)
		output = self.limitTwoWords(output)
		output = output.rstrip()
		return output

def returnCleanData(oldFilename, newFilename):

	dataOld = NCM(oldFilename, datetime.fromtimestamp(os.path.getmtime(oldFilename)).strftime('%Y-%m-%d'))
	dataOld.removeSpaces()

	dataNew = NCM(newFilename, datetime.fromtimestamp(os.path.getmtime(newFilename)).strftime('%Y-%m-%d'))
	dataNew.removeSpaces()

	savingData = NCM(None)
	savingData.data = pd.concat([dataOld.data, dataNew.data]).drop_duplicates(subset=['DESCRICAO DO INSUMO', 'PRECO MEDIANO R$'], keep='last')
	
	return savingData.data

