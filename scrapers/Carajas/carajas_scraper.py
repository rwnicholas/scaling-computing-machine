from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import lxml.html as parser
import requests

class CarajasScrapper(object):
    """
    Class used for scrapping the website https://www.carajasonline.com/, specifically to find products. 
    """
    driver = 0
    html = ""

    basePage = "https://www.carajasonline.com/"

    localhostUrl = "http://127.0.0.1:8000/api/"

    items=[]

    storeName = "Carajás"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')

        self.driver = webdriver.Chrome(options=options)
        
        self.driver.maximize_window()
        self.driver.get(self.basePage)
        self.oldUrl=self.basePage
        
        self.html = parser.fromstring(self.driver.page_source)

    def compareIfDifferentUrls(self, url1, url2):
        """
        Compare two urls.
        """
        return url1!=url2

    def saveAPI(self):
        """
        Send data from items to the API at http://127.0.0.1:8000/api/.
        """

        print("Saving on API ------")
        # print("\nlen Items: ", len(self.items),"\n")

        for map in self.items:

            payload = map

            # primeiro procurando saber se o produto ja existe:
            try:
                print("\n...Getting product...")
                urlGet = self.localhostUrl+"%s/" %map["id"]
                response = requests.get(urlGet)
            except Exception as e:
                print("Exception on getting product! Error: ", e)
                
            if(response.status_code!=404): # se houver o produto na api, eh so atualizar
                try:
                    print("\n...Updating product...")
                    putUrl = self.localhostUrl+"%s/" %map['id']
                    response = requests.put(putUrl, data=payload)
                except Exception as e:
                    print("Exception on putting product! Error:  ", e)
            else: #se nao houver produto com o id, ele eh novo para o bd
                try:
                    print("\n...Posting product...")
                    response = requests.post(self.localhostUrl, data=payload)
                    if(response.status_code==400):
                        print("\nresponse content: %s\n" %response.content)
                except Exception as e:
                    print("Exception ", e)

    def separateData(self, text:str):
        """
        Receives a long text like ```"Cimento 5kg Cód. 5412 R$ 6,00"``` and converts it to a map
        separating important data like: ```{"description":"Cimento 5kg", "id":"5412", price:"6,00"}```
        """
        textList = text.split()

        idIndex = 0
        priceIndex = 0
        for i in range(len(textList)):
            if(textList[i].lower()=="cód."):
                idIndex=i+1
            elif(textList[i]=="R$"):
                priceIndex=i+1
        if(len(textList)>0):
            description= ' '.join(textList[:idIndex-1]) #-1 para n add a palavra "cod"
            code = textList[idIndex]
            priceList = textList[priceIndex].split(",") # separando pela virgula p/ mudar p ponto
            price = '.'.join(priceList)
            
            try:
                return {
                    "description":description,
                    "price":float(price),
                    "id":code,
                    "storeName":self.storeName,
                    "brand":"",
                    "notes":"Nothing",
                }
            except Exception as e:
                print("Error on converting final map. Error: ", e)
                
        else:
            return None

    def findProductByDescription(self, description):
        """
        Search for a product with a given description.\n
        :param description: part of description of a product.
        
        """

        print("Manipulating input...\n")
        inputXpath = "//fieldset[@class='busca']/input[@type='text']"

        WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,inputXpath)))
        
        inputElement = self.driver.find_element_by_xpath(inputXpath)
        inputElement.clear() #para limpar um possivel rotulo que esteja no input
        inputElement.send_keys(description)
        searchButton = self.driver.find_element_by_xpath("//input[@class='btn-buscar']")
        searchButton.click()

        print("Comparing urls ...\n")
        WebDriverWait(self.driver, 20).until(lambda x : self.compareIfDifferentUrls("https://www.carajasonline.com/", self.driver.current_url))
        
        #atualizando html:
        self.html = parser.fromstring(self.driver.page_source)

        print("Getting product... \n")
        try:
            # searchedProductsList ="//div[@class='col-md-12 cb-prateleira-product-name']"
            searchedProductsList  = "//div[@class='cb-prateleira-departament n4colunas']/ul/li"
            products = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH,searchedProductsList)))
        except:
            print("Timeout on getting products")
            return {'error':'None object found'}

        firstProductText = products[0].text
        productTextList = firstProductText.split()

        print("first produt text: ", firstProductText)

        description = ""
        price=0
        for i in range(len(productTextList)):
            if(productTextList[i]!="R$"):
                description+=productTextList[i]+" "
            else:
                price =productTextList[i+1] 
                break

        return {'description': description, 'price':price}

    def scrapAllProducts(self, getDefaultUrl=True):
        """
        Goals to scrap all products is possible in building materials department.
        """
        print("Scrapping all products...")
        
        if(getDefaultUrl):
            self.driver.get("https://www.carajasonline.com/construcao/material-de-construcao")
            self.html = parser.fromstring(self.driver.page_source)

        try:
            allProductsXpath = "//div[@class='cb-prateleira-departament n4colunas']/ul/li"
            products = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH,allProductsXpath)))
        except:
            print("Timeout on getting products")
            return {'error':'None object found'}
        
        print("len prod:" , len(products))

        for product in products:
            item = self.separateData(product.text)
            if(item!=None):
                self.items.append(item)

        try:
            currentPageXpath = "//div[@class='pager bottom']/ul[@class='pages']/li"
            pages = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH,currentPageXpath)))

        except:
            print("Timeout: Cant find pages anymore!")

        #### as linhas abaixo sao para ir para a prox pagina:

        pagesNumbers = [] #sem os items "ultimo","primeiro"...
        currentPageIndex =0
        #tirar os botoes de proximo e ultimo
        for i in range(len(pages)):
            classAttr = pages[i].get_attribute("class")
            if(classAttr=="page-number pgCurrent" or classAttr=="page-number"):
                pagesNumbers.append(pages[i])
            
        for i in range(len(pagesNumbers)):
            classAttr = pagesNumbers[i].get_attribute("class")
            # encontrar a pagina atual
            classes = classAttr.split()
            if("pgCurrent" in classes):
                currentPageIndex = i

        print("Curr: ", currentPageIndex, "pages numbers: ", pagesNumbers)
        if(currentPageIndex<(len(pagesNumbers)-1)):
            idNextPage = pagesNumbers[currentPageIndex+1].text

            baseUrl = "https://www.carajasonline.com/construcao/material-de-construcao"
            nextUrl = baseUrl+"#"+idNextPage
            self.driver.get(nextUrl)
            self.driver.refresh()
            print("\n new url: ", self.driver.current_url)

            self.html = parser.fromstring(self.driver.page_source)  
            try:
                self.scrapAllProducts(getDefaultUrl=False)
            except:
                print("Cant scrapy anymore")


        self.saveAPI()

        return self.items


# def main():
#     print("Main!")
#     scrapper = CarajasScrapper()
#     # result = scrapper.findProductByDescription("cimento 5kg")
#     # print("result ", result)
#     items = scrapper.scrapAllProducts()
#     print("\nLenght of items:",len(items),"\nItems:\n", items)


# main()
    
