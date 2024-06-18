import os
from django.apps import AppConfig
from django.conf import settings


class MongodbOrmConfig(AppConfig):
    name = 'mongodb_orm'

    def ready(self):
        if hasattr(settings, 'MONGODB_ORM_MODELS_FOLDER'):
            absolute_path = os.path.abspath(settings.MONGODB_ORM_MODELS_FOLDER)
            if not os.path.exists(absolute_path):
                os.makedirs(absolute_path)
                print(f"Model directory '{absolute_path}' created successfully.")
