import os
import sys
import importlib.util
from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from mongodb_orm.interfaces.mongodb_model import MongoDBModel
from mongodb_orm.views.mongodb_api_model_view import MongoDBAPIModelView

current_directory = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = settings.BASE_DIR
if hasattr(settings, 'MONGODB_ORM_MODELS_FOLDER'):
    MONGODB_MODELS_PATH = settings.MONGODB_ORM_MODELS_FOLDER
else:
    MONGODB_MODELS_PATH = "app/models"

models_directory = os.path.join(current_directory, BASE_DIR, MONGODB_MODELS_PATH)
sys.path.insert(0, os.path.abspath(os.path.join(current_directory, "..")))

router = routers.SimpleRouter()

for filename in os.listdir(str(models_directory)):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = os.path.splitext(filename)[0]
        try:
            module = importlib.import_module(f"{MONGODB_MODELS_PATH.replace('/', '.')}.{module_name}")
            for name, obj in vars(module).items():
                if (isinstance(obj, type) and issubclass(obj, MongoDBAPIModelView)
                        and issubclass(obj, MongoDBModel) and obj != MongoDBAPIModelView and obj != MongoDBModel):
                    router.register(rf"{obj.collection_name}", obj, basename=f"{obj.collection_name}")
        except Exception as e:
            print(f"Error loading module {module_name}: {e}")

BREAD_URLS = [
    path('', include(router.urls)),
]
