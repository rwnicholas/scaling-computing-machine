class Router:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'sinapi':
            return 'sinapi'
        elif model._meta.app_label == 'EcoAL':
            return 'economiza_al'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'sinapi':
            return 'sinapi'
        elif model._meta.app_label == 'EcoAL':
            return 'economiza_al'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'sinapi' or obj2._meta.app_label == 'sinapi':
            return True
        elif 'sinapi' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        elif obj1._meta.app_label == 'EcoAL' or obj2._meta.app_label == 'EcoAL':
            return True
        elif 'EcoAL' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'sinapi':
            return db == 'sinapi'
        elif app_label == 'EcoAL':
            return db == 'economiza_al'
        return 'default'