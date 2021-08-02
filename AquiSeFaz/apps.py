from os import name
from django.apps import AppConfig
import django


class AquisefazConfig(AppConfig):
    name = 'AquiSeFaz'

    def ready(self):
        from AquiSeFaz.updater import EcoALUpdater,SinapiUpdater, PortalGovUpdater, ecoal, sinapi, portalCompras
        
        ecoUp = EcoALUpdater()
        ecoUp.start()
        # print(ecoal())
        
        sinapiUp = SinapiUpdater()
        sinapiUp.start()
        # print(sinapi())
        
        pGov = PortalGovUpdater()
        pGov.start()
        # print(portalCompras())