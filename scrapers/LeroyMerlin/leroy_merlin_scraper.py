from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By #parara poder enviar dados num input
import lxml.html as parser
import csv
import requests

class LeroyMerlinScrapper(object):
    """
    A class for scrapping the page at http://leroymerlin.com.br/. For use it starts calling navigationToDepartments().
    """
    
    driver=0
    html=""

    # comecando da parte de tijolos
    basePage = "https://www.leroymerlin.com.br/materiais-de-construcao"

    items=[]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('windows-size=1920x1080')

        self.driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')

        self.driver.maximize_window()
        # comecando do primeiro departamento
        self.driver.get(self.basePage)

        self.html = parser.fromstring(self.driver.page_source)

        self.getLocalizeInput()

        self.html = parser.fromstring(self.driver.page_source)

    def saveCsv(self):
        """
        Save the data on a .csv file.
        """

        #verificar se ja ha linhas
        file = open("items.csv", encoding='utf8')
        reader = csv.reader(file)
        lines = len(list(reader))
        print("Lines:", lines)

        #escrever novos arquivos
        keys = self.items[0].keys()
        with open("items.csv", 'a', encoding='utf8') as f:
            dict_writer = csv.DictWriter(f, keys)

            if(lines == 0):
                dict_writer.writeheader()

            dict_writer.writerows(self.items)

    def convertPriceFromMillionNumber(self, priceDigitsList):
        """
        Converts a number from 1.899 to 1,999, form accepted in us languages.\n
        :param priceDigitsList: a list containing price's number in another format, specifically pt-br format,
        separated for decimal part and a possible hundred or bigger part.\n
        :return: a float
        
        ``Example:``
            priceDigitsList: [1.999,10]
            return: 1999.10
        """

        thousandNumber = ""
        thousandNumbers = priceDigitsList[0].split('.')
        for number in thousandNumbers:
            thousandNumber+=number
        return float(thousandNumber+"."+priceDigitsList[1])
        

    def saveAPI(self):
        """
        Save data in API at http://127.0.0.1:8000/products/.
        """

        for map in self.items:
            priceList = map["price"].split(",")
            
            payload = {
                "description": map["name"],
                "price": self.convertPriceFromMillionNumber(priceList),
                "storeName": "Leroy Merlin",
                "notes":"none"
            }
            response = requests.post("http://127.0.0.1:8000/products/", data=payload)

            print("Response: ", response.content)

    def parseItems(self, listNameItems, listIntegerPrices, listDecimalItems):
        """
        Parses the received lists to a map inside self.items containing fields 'name' and 'price' of the product.\n
        :param listNameItems: a list containing product's name.\n
        :param listIntegerPrices: a list containing product's price, specifically integer part.\n
        :param listDecimalItems: a list containing product's price, specifically decimal part.\n
        
        ``Example:``
            listNameItems: ['Cimento 5kg', 'Tijolo 4 furos']
            listIntegerPrices: [50,7]
            listDecimalItems: [75,90]
        """

        if(len(listNameItems)==len(listIntegerPrices)):
            for index in range(len(listNameItems)):
                self.items.append(
                    {
                        'name': listNameItems[index],
                        'price': listIntegerPrices[index]+listDecimalItems[index]
                    }
                )
                # print("\n item no indice: ", self.items[index])
            print("Items:", self.items)
        else:
            print("\nDifferent sizes!")
            print("\nNames length:", len(listNameItems))
            print("\nInteger lenght:", len(listIntegerPrices))



    def saveScreenshot(self):
        """
        Save an image from the current screen of the webdriver.
        """

        saved = self.driver.save_screenshot("../../screenshots/leroy-merlin.png")
        print("Screenshot saved! ",saved)


    def getLocalizeInput(self):
        """
        Handles a popup asking for user's localization and send Maceió as the localization.\n
        """
        print("\n Getting localization \n")

        try:

            # Procurando o elemento de entrada do nome da cidade e "digitando" o nome maceió neste elemento
            WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@name='city']")))
            inputElement = self.driver.find_element_by_xpath("//input[@name='city']")
            inputElement.send_keys("Maceió")

            # Aguardando até que o nome sugerido com o nome da cidade digitado apareca
            WebDriverWait(self.driver,20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='Suggestion-bkx3x4-7 hkAiIc']/div[@class='SuggestionItem-bkx3x4-8 fzfVtZ']")))
            
            # Pegando o nome sugerido e clicando nele
            labelSuggestedLocalization = self.driver.find_element_by_xpath("//div[@class='Suggestion-bkx3x4-7 hkAiIc']/div[@class='SuggestionItem-bkx3x4-8 fzfVtZ']")
            labelSuggestedLocalization.click()

            # Aguardando até que o botão de confirmar apareça
            WebDriverWait(self.driver,20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='SecondStep-bkx3x4-11 fFugBA']/button")))
            
            # Pegando o botão e clicando nele para que possa ir para a página indicada na basePage
            submitButton = self.driver.find_element_by_xpath(
                "//div[@class='SecondStep-bkx3x4-11 fFugBA']/button")
            
            submitButton.click()

            print("\n URL====> ", self.driver.current_url)
            self.saveScreenshot()

            print("\n Finishing get localization \n")
        except Exception as e:
            print("Error on getting local input. Error msg: ", e)

    def navigationToDepartments(self):
        """
        Responsible to find and navigate to each department on the website, sending later to the responsible
        methods to handle with data in the departments.
        """

        print("\n------NAVIGATION TO DEPARTMENTS METHOD------\n")
        self.html = parser.fromstring(self.driver.page_source)
        departments = self.html.xpath(
            "//div[@class='swiper-wrapper']/div/div/div/a/@href")

        print("Found %d departments!" %(len(departments)))

        for index in range(len(departments)):
            self.driver.get(departments[index])
            self.scrapPages()
        print("\n------ENDING NAVIGATION TO DEPARTMENTS METHOD------\n")

    def goToProductDetailsPage(self):
        print("\n------PRODUCT DETAILS PAGE------\n")

        self.html = parser.fromstring(self.driver.page_source)

        idXpath = "//div[@class='badge product-code badge-product-code']"

        try:
            idList = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH,idXpath)))
        except:
            print("Timeout on getting products")
            return {'error':'None object found'}

        print("Id: ", idList[0].text)

        titleXpath = "//div[class='product-title-container']/h1/text()"
        title = self.html.xpath(titleXpath)
        priceIntegerXpath = "//div[@class='to-price']/span[@class='price-integer']/text()"
        priceDecimalXpath = "//div[@class='to-price']/span[@class='price-decimal']/text()"

        # priceInteger
        # priceDecimalWithoutComma = priceDecimalXpath.split(',')[0]
        # priceString = priceIntegerXpath+priceDecimalWithoutComma


    def scrapOnePage(self):
        """
        Search for products in one page at a time. It will find info like price, title, etc.
        """

        print("\n------SCRAP ONE PAGE METHOD------\n")
        self.html = parser.fromstring(self.driver.page_source)

        print("\nURL ->", self.driver.current_url)

        baseProductXpath = "//div[@data-products-container='']"

        try:
            productsXpath = baseProductXpath+"/div"
            products = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH,productsXpath)))
            print("found ps: ", products)
        except:
            print("Timeout on getting products")
            return {'error':'None object found'}

        for p in products:
            print("Clicking on product...")
            p.click()
            self.goToProductDetailsPage()

        print("\nLen products:", len(self.html.xpath(baseProductXpath)), "\n products: ", self.html.xpath(baseProductXpath))

        productNames = self.html.xpath(
            baseProductXpath+"/div/@title")

        # teste = baseProduct + \
        #     "/div/figure[@class='row']/div[@class='price-tag  ']"

        # print("\nLen prices:", len(self.html.xpath(teste)), "\n prices: ", self.html.xpath(teste))

        priceBase = baseProductXpath + \
            "/div/figure[@class='row']/div[@class='price-tag  ']/div/div[@class='to-price-container']/div[@class='to-price']"
        
        productIntegerPrices = self.html.xpath(priceBase+"/span[@class='price-integer']/text()")
        productDecimalPrices = self.html.xpath(priceBase+"/span[@class='price-decimal']/text()")
        

        print("\nProducts: ", productNames, "\n tamanho: ", len(productNames))

        print("\n PRICES \ninteger: ", productIntegerPrices, "\ndecimal: ", productDecimalPrices)

        self.parseItems(productNames, productIntegerPrices, productDecimalPrices)

        # self.saveCsv()
        print("\n---SAVING ON API---\n")
        self.saveAPI()

        print("\n------ENDING SCRAP ONE PAGE METHOD------\n")

    def scrapPages(self):
        """
        Search for products list on the page. It will find a 
        list of product variety, and just then a list with that products.
        """


        print("\n------SCRAP PAGES METHOD------\n")
        print("\n URL in scrapping pages:", self.driver.current_url)
        self.html = parser.fromstring(self.driver.page_source)
        self.saveScreenshot()
        
        typeProductsXpath = "//div[@class='swiper-wrapper']/div/div/div/a/@href"
        
        try:
            print("Waiting for type products...")
            WebDriverWait(self.driver,20).until(EC.presence_of_all_elements_located((By.XPATH, typeProductsXpath)))
        except:
            print("Timeout waiting for type products")


        typeProductsBlock = self.html.xpath(typeProductsXpath)

        print("List:", typeProductsBlock)
        
        for index in range(len(typeProductsBlock)):
            self.driver.get(typeProductsBlock[index])
            print("\n URL in for:", self.driver.current_url)
            self.html = parser.fromstring(self.driver.page_source)
            containerAllProducts = self.html.xpath("//div[@data-products-container='']")
            if(len(containerAllProducts)>0):
                print("Going to scraping products")
                self.scrapOnePage()  
            else:
                print("\n Going to scrapping pages for the 2nd time!")
                self.scrapPages()

        print("\n------ENDING SCRAP PAGES METHOD------\n")

# def main():
#     scrapper = LeroyMerlinScrapper()
#     scrapper.navigationToDepartments()

# main()
