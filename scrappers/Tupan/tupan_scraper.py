from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import lxml.html as parser
from selenium.common.exceptions import TimeoutException
import requests
from datetime import date


class TupanScrapper():
    """
    A class for scrapping the website https://www.tupan.com.br/. For use it starts calling scrapPage() method.
    """

    html = ""  # sera do tipo string mesmo
    driver = 0
    items = []

    basePage = "https://www.tupan.com.br/"
    baseXpath = "//div[@class='products-list__item']/div[@class='product-card product-card-logged']/"

    departments = ["materiais-de-construcao"]

    region = "al" #must be in lowercase

    def __init__(self):
        self.setScrapperConfigurations()

    
    def setScrapperConfigurations(self):
        """
        Initial settings to the scrapper.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("windows-size=1920x1080")

        self.driver = webdriver.Chrome(options=options)

        self.driver.maximize_window()
        self.driver.get(
            self.basePage + self.departments[0]
        )  # comecando do primeiro departamento

        self.html = parser.fromstring(self.driver.page_source)

        self.setLocalization()

    def checkRegion(self, placeOptionsLabelsList):
        """
        Checks if the string 'pe' (pernambuco) is in the place options list given.
        """
        counterIndex = 0
        for place in placeOptionsLabelsList:
            if (self.region in place.lower()): 
                return counterIndex
            counterIndex += 1

        return counterIndex

    def setLocalization(self):
        """
        Set the localization (Maceio) asked for the website on first use.
        """
        print("0. Setting localization ------")
        modalLocalization = self.html.xpath("//div[@class='modal-body']")

        if(len(modalLocalization)>0):
            placeListString = "//div[@class='modal-body']/div[@class='text-center']/div"

            WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, placeListString)))

            placeOptionsList = self.driver.find_elements_by_xpath(placeListString)
            placeOptionsLabelsList = self.html.xpath(placeListString+"/a/text()")

            index = self.checkRegion(placeOptionsLabelsList)

            print(" localization: ",placeOptionsLabelsList[index])

            placeOptionsList[index].click()

    def saveScreenshot(self):
        """
        Save an image of the screen at the moment is called.
        """

        self.driver.save_screenshot("../../screenshots/screenshotTupan.png")

    def splitPriceFieldBetweenIntegerAndDecimal(self, map):
        """
        Separate the digits at a number inside a given map containing a 'price' key, excluding labels like "each".\n
        :param map: is a map containing a price key.\n
        :return: a list with just the numbers of price.\n

        ``Example``: {'price':'18.90 cada'} returns [18,90]
        """

        # convertendo o dado que vem da parte de preco para lista: 18,90 cada -> ["18,90","cada"]
        listSplitPrice = map["price"].split()

        # tirando o texto do preco e separando os digitos do preco: ["18,90","cada"] -> [18,90]
        listPriceJustNumbers = listSplitPrice[1].split(",")

        return listPriceJustNumbers

    def convertPriceFromMillionNumber(self, priceDigitsList):
        """
        Converts a number from 1.899 to 1,999, form accepted in us languages.\n
        :param priceDigitsList: a list containing price's number in another format, specifically pt-br format.\n
        :return: a float
        
        """

        # separando um possivel numero do milhar: [1.899] -> [1,889]
        millionNumberList = priceDigitsList[0].split(".")

        # criando uma nova string sem a pontuacao com a primeira parte do preco: [1,889] -> 1889
        priceFirstDigit = ""
        for number in millionNumberList:
            priceFirstDigit += number

        # concatenando o primeiro com o segundo digito do preco (o segundo digito estara na lista passada)
        price = float(priceFirstDigit + "." + priceDigitsList[1])

        return price

    def convertItemFieldsToAPI(self, map):
        """
        Converts item from a map to the API format, specifically a tuple containing notes and price.\n
        :param map: a map containing field price.\n
        :return: a tuple with a note and price fields, respectivelly.
        """

        priceDigitsList = self.splitPriceFieldBetweenIntegerAndDecimal(map)

        # inicializando as variaveis
        notes = "none"
        price = 0

        # Verificando se o texto contido no lugar do preco eh realmente um preco (produto esta disponivel)
        # ou se esta fora de estoque
        if len(priceDigitsList) == 1:
            price = 0
            notes = "out of stock"
        else:
            price = self.convertPriceFromMillionNumber(priceDigitsList)

        return (notes, price)

    def saveAPI(self):
        """
        Send data from items to the API at http://127.0.0.1:8000/api/.
        """

        print("6. Saving on API ------")
        print("\nlen Items: ", len(self.items),"\n")

        for map in self.items:
            notesPriceTuple = self.convertItemFieldsToAPI(map)  
            codeNumber = map["code"].split()[1]

            payload = {
                "id": int(codeNumber),
                "description": map["description"],
                "price": notesPriceTuple[1],
                "storeName": "Tupan",
                "notes": notesPriceTuple[0],            
            }

            try:
                response = requests.post("http://127.0.0.1:8000/api/", data=payload)
                print("response: ", response.status_code)
            except Exception as e:
                print("Exception ", e)


            # print("Response: ", response.content)

    def parseOneItem(self, listDescription, listPrice, listCodes):
        """
        Parses one list of items at a time, since then the program select a lot of lists along the execution.\n
        :param listDescription: a list with the item's descriptions.\n
        :param listPrice: a list with the item's prices.\n
        
        """

        print("5. Parsing just one item ------")
        # aqui, o tamanho da lista de descricoes de produto eh utilizado pq tanto fazia usar
        # o tamanho dela ou dos precos, ja que eh a mesma quantidade

        if(len(self.items)>0):
            print("len list description: ", len(listDescription))
            print("len list codes: ", len(listCodes))
            # newList = listDescription[len(self.items):]
            # print("new list",len(newList))
            for index in range(len(self.items),len(listDescription)):
                print("elemento : ", index)
                self.items.append(
                    {"description": listDescription[index], "price": listPrice[index], "code": listCodes[index]}
                )
        else:
            for index in range(len(listDescription)):
                self.items.append(
                    {"description": listDescription[index], "price": listPrice[index], "code": listCodes[index]}
                )

    def parseItems(self):
        """
        Goals to find and parse the items in the page.
        """

        print("4. Parsing items ------")

        self.html = parser.fromstring(self.driver.page_source)

        #baseXpath = "//div[@class='products-list__item']/div[@class='product-card product-card-logged']/"

        descriptions = self.html.xpath(
            "//div[@class='product-card__name']/a/text()"
        )

        print("len descriptions: ", len(descriptions))

        prices = self.html.xpath(
            "//div[@class='product-card__new-price']/text()"
        )

        codes = self.html.xpath(
             "//div[@class='product-card__rating-legend mt-1']/text()"
        )

        if(len(descriptions)==len(prices) and len(prices)==len(codes)):
            self.parseOneItem(
                descriptions, prices, codes
            )  # convertendo os diferentes atributos para um item na tabela
        else:
            print("\n Cannot parse itens: Lenght different")


    def hasMoreScroll(self):
        """
        Checks if the page has scroll yet.\n
        ``Return``: a boolean
        """

        print("3. Checking scroll ------")
        pageHeight = self.driver.execute_script("return document.body.scrollHeight")
        totalScrolledHeight = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
        print("pageHeight: %f | totalScrolled: %f" %(pageHeight,totalScrolledHeight))
        
        # pq -1?
        if (pageHeight) <= totalScrolledHeight: #quando o tanto scrollado eh igual ao tamando da pagina
            return False
        else:
            return True

    def scrollDownThePage(self):
        """
        Scrolls the page equals to page height.
        """

        print("2. Scrolling down ------")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scrapPage(self):
        """
        Responsible for check the products quantity gotten from the scrapping and call the responsible methods for
        each operation for scrapping the page.
        """

        print("1. Scrapping page ------")
        # Alinha abaixo esta buscando o elemento que diz quantos itens ha, pegando ele da lista que eh retornada
        # dando um split pra pegar apenas o numero (ja que eh um texto) e pegando esse numero (primeiro elemento -> 0)

        for department in self.departments:

            self.driver.get(self.basePage + department)
            self.html = parser.fromstring(self.driver.page_source)
            
            quantityContainer = self.html.xpath("//div[@class='view-options__control']/label/text()")
            print("container:", quantityContainer)
            quantity=0
            if(len(quantityContainer)>0):
                productsQuantityDescription = quantityContainer[0].split()
                quantity = int(productsQuantityDescription[0])
            
            print("Quantity: ", quantity)

            self.items = []  # zerando a lista de itens pq ela eh construida por departamento

            while len(self.items) < quantity:
                if (len(self.items) >= quantity):  # para nao pegar itens repetidos
                    break
                else:
                    try:
                        self.scrollDownThePage()

                        WebDriverWait(self.driver, 30).until(
                            lambda driver: self.hasMoreScroll()==False
                        )

                        self.parseItems()

                    except TimeoutException:
                        break  # pra brekar apenas esse while, n o for

            self.saveAPI()

# def main():
#     scrapper = TupanScrapper()
#     scrapper.scrapPage()


# main()
