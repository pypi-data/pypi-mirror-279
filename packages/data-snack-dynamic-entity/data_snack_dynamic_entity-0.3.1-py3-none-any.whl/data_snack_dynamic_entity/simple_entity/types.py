from typing import TypedDict, Dict, Any


class FieldSchema(TypedDict):
    type: str
    key: bool
    excluded: bool
    optional: bool
    default: Any


class SimpleEntitySchema(TypedDict):
    properties: Dict[str, FieldSchema]
    version: int
    type: str


SimpleEntityTemplates = Dict[str, SimpleEntitySchema]
