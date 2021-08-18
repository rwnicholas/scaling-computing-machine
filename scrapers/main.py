from Carajas.carajas_scraper import CarajasScrapper
from Tupan.tupan_scraper import TupanScrapper
from LeroyMerlin.leroy_merlin_scraper import LeroyMerlinScrapper

class Main:
    tupan = TupanScrapper()
    # leroy = LeroyMerlinScrapper() # comentada por motivos de: em atualizacao
    carajas_scraper = CarajasScrapper()

    def run(self):
        print("Runing!")
        print("\n\n1 - Tupan scrapper starting now!")
        self.tupan.scrapPage()
        print("\n\n2 - Carajas scrapper starting now!")
        self.carajas_scraper.scrapAllProducts()
        # print("\n\n3 - Leroy scrapper starting now!")
        # self.leroy.scrapPages()

def init():
    m = Main()
    m.run()

init()
