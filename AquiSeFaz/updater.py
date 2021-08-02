#!/usr/bin/python3
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from EcoAL.views import ecoal
from sinapi.views import sinapi
from PortalComprasGov.views import portalCompras

class EcoALUpdater:
    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(ecoal, 'interval', days=3)
        scheduler.start()

class SinapiUpdater:
    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(sinapi, 'interval', weeks=4)
        scheduler.start()
    
class PortalGovUpdater:
    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(portalCompras, 'interval', weeks=4)
        scheduler.start()
