from abc import ABCMeta, abstractmethod


class Scraper(object, metaclass=ABCMeta):

    @abstractmethod
    def saveAPI(self):
        pass

    @abstractmethod
    def parseOneItem(self, *args):
        pass

    @abstractmethod
    def parseItems(self, *args):
        pass

    @abstractmethod
    def crawPage(self):
        pass

    @abstractmethod
    def setCrawlerConfigurations(self):
        pass
