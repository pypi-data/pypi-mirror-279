from typing import Dict, Union

from data_snack_dynamic_entity.compound_entity.types import CompoundEntitySchema
from data_snack_dynamic_entity.simple_entity.types import SimpleEntitySchema

EntityTemplates = Dict[str, Union[SimpleEntitySchema, CompoundEntitySchema]]
