from typing import TypedDict, Dict, List


class SourceEntityFieldSchema(TypedDict):
    field: str
    source_field: str


class SourceEntitySchema(TypedDict):
    entity: str
    fields: List[SourceEntityFieldSchema]


class CompoundEntitySchema(TypedDict):
    type: str
    sources: List[SourceEntitySchema]


CompoundEntityTemplates = Dict[str, CompoundEntitySchema]
