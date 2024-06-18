import inspect
import pkgutil
import importlib
from typing import Union, List, Callable
from django.core.management import BaseCommand
from mongodb_orm.types.options import ValidationLevel
from mongodb_orm.interfaces.mongodb_model import MongoDBModel
from mongodb_orm.singletons.mongodb_singleton_client import MongoDBClient


class Command(BaseCommand):
    help = """
        Update a specific schema, or update the schema for all collections if a schema is not explicitly provided.
        If a collection model is specified, the command will update the schema for that collection;
        otherwise, the command will iterate over all collections in the database, updating their schemas.
    """

    @staticmethod
    def find_class_in_module(module, class_name):
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__name__ == class_name:
                return obj
        return None

    @staticmethod
    def find_all_classes_in_module(module):
        return [obj for _, obj in inspect.getmembers(module) if inspect.isclass(obj)
                and obj.__module__ == module.__name__
                and obj.__name__.endswith("Model")]

    def find_classes_in_package(self, package_name, class_name=None) -> Union[Callable, List[Callable], None]:
        package = importlib.import_module(package_name)

        if class_name:
            # Find a specific class in the package
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                module_path = f"{package_name}.{module_name}"
                module = importlib.import_module(module_path)
                dynamic_class = self.find_class_in_module(module, class_name)
                if dynamic_class:
                    return dynamic_class
            return None

        # Find all classes within the package
        all_classes = []
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module_path = f"{package_name}.{module_name}"
            module = importlib.import_module(module_path)
            classes_in_module = self.find_all_classes_in_module(module)
            all_classes.extend(classes_in_module)

        return all_classes

    def update_schema(self, tenant, collection_model: MongoDBModel):
        client = MongoDBClient().get_database(f'{tenant}')
        if collection_model.options and 'schema' in collection_model.options:
            validation_level: str = ValidationLevel.STRICT.value
            if 'validation_level' in collection_model.options:
                validation_level: str = ValidationLevel(collection_model.options['validation_level']).value
            client.command('collMod', collection_model.collection_name,
                           validator=collection_model.options['schema'],
                           validationLevel=validation_level)
            self.stdout.write(self.style.SUCCESS(f'Done schema updating for : {collection_model.collection_name}'))
        else:
            self.stdout.write(self.style.WARNING(
                f'No schema specified for Collection , skip schema updating: {collection_model.collection_name}'))

    def add_arguments(self, parser):
        parser.add_argument('collection_model', nargs='?', type=str, help='The collection model to update')
        parser.add_argument('tenant', nargs='?', type=str,
                            help='The tenant for the model to update, if empty use public')

    def handle(self, *args, **options):
        tenant = options['tenant'] if options['tenant'] else 'public'
        collection_model = options['collection_model']
        if collection_model is not None:
            dynamic_class = self.find_classes_in_package("mongodb_orm.models", collection_model)

            if dynamic_class:
                dynamic_instance = dynamic_class(tenant)
                self.stdout.write(
                    self.style.SUCCESS(f'Starting schema update for : {dynamic_instance.collection_name}'))
            else:
                self.stdout.write(self.style.ERROR(f"Module '{collection_model}' does not exist."))
        else:
            self.stdout.write('Start updating all schema for Tenant')
            dynamic_classes = self.find_classes_in_package("mongodb_orm.models")
            for dynamic_class in dynamic_classes:
                dynamic_instance = dynamic_class()
                self.stdout.write(self.style.SUCCESS(f'Start schema update for : {dynamic_instance.collection_name}'))
                self.update_schema(tenant, dynamic_instance)
