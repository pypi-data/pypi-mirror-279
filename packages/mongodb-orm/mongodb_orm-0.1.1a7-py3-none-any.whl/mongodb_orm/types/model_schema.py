from enum import Enum
from typing import TypedDict, List, Dict, Optional, Union, Final


class GeoJsonType(Enum):
    POINT: Final[str] = 'Point'
    LINESTRING: Final[str] = 'LineString'
    POLYGON: Final[str] = 'Polygon'
    MULTIPOINT: Final[str] = 'MultiPoint'
    MULTILINESTRING: Final[str] = 'MultiLineString'
    MULTIPOLYGON: Final[str] = 'MultiPolygon'


class PropertySchema(TypedDict):
    bsonType: str
    description: Optional[str]  # Optional
    required: Optional[List[str]]  # Optional
    properties: Optional[Dict[str, 'PropertySchema']]  # Optional


class ModelSchema(TypedDict):
    bsonType: str
    title: Optional[str]  # Optional
    required: Optional[List[str]]  # Optional
    properties: Dict[str, Union[PropertySchema, dict]]  # Optional
