from uuid import UUID
from bson import ObjectId
from django.db.models import Model
from datetime import datetime, date


class Helper:
    @classmethod
    def standardize_dict(cls, dct: dict, underscore=False) -> dict:
        standard_dct = {}
        for key, value in dct.items():
            # if key == '_id':
            #     standard_dct['id'] = str(value)
            if key.startswith('_') and not underscore:
                continue
            if isinstance(value, dict):
                standard_dct[key] = cls.standardize_dict(value)
                continue
            if isinstance(value, UUID):
                standard_dct[key] = value.hex
                continue
            if isinstance(value, list):
                standard_dct[key] = [str(obj_id) if isinstance(obj_id, ObjectId) else obj_id for obj_id in value]
                continue
            if isinstance(value, ObjectId):
                standard_dct[key] = str(value)
                continue
            if isinstance(value, (datetime, date)):
                standard_dct[key] = value.isoformat()
                continue
            if isinstance(value, Model):
                standard_dct[key] = value.pk if not isinstance(value.pk, UUID) else value.pk.hex
                continue
            standard_dct[key] = value

        return standard_dct

    @classmethod
    def standard_record(cls, dct: dict) -> dict:
        standard_dct = {}
        for key, value in dct.items():
            if isinstance(value, dict):
                standard_dct[key] = cls.standard_record(value)
                continue
            if isinstance(value, list):
                new_list = []
                for obj in value:
                    if isinstance(obj, dict):
                        new_list.append(cls.standard_record(obj))
                    else:
                        new_list.append(obj)
                standard_dct[key] = new_list
                continue
            if key == '@type' and value == 'id':
                standard_dct = ObjectId(dct['@value'])
                continue
            if key == '@value':
                continue
            standard_dct[key] = value
        return standard_dct

