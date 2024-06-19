from dataclasses import dataclass, field, make_dataclass, MISSING
from typing import Dict, Type, List

from data_snack.entities.compound import CompoundEntity
from data_snack.entities.exceptions import SourceEntityFieldException
from data_snack.entities.models import SourceEntity, EntityFieldMapping

from data_snack_dynamic_entity.compound_entity.exceptions import NonExistingSourceEntityException
from data_snack_dynamic_entity.compound_entity.types import CompoundEntitySchema, CompoundEntityTemplates
from data_snack_dynamic_entity.validate import validate_entity_templates


def create_source_entity_field_mappings(entity_schema: CompoundEntitySchema) -> Dict[str, List[EntityFieldMapping]]:
    """
    Creates source entity field mappings according to given schema.

    :param entity_schema: new entity schema
    :returns: source and new entity field mappings
    """
    return {
        source["entity"]: [
            EntityFieldMapping(
                field=field_mapping["field"],
                source_field=field_mapping["source_field"]
            )
            for field_mapping in source["fields"]
        ]
        for source in entity_schema["sources"]
    }


def create_source_entities(
        source_entities: Dict[str, Type], source_entities_fields_mapping: Dict[str, List[EntityFieldMapping]]
) -> List[SourceEntity]:
    """
    Creates source entities according to source entity field mappings.

    :param source_entities: source entity objects
    :param source_entities_fields_mapping: source entity field mappings
    :returns: source entities for new entity
    """
    try:
        sources = [
            SourceEntity(
                entity=source_entities[entity],
                entity_fields_mapping=fields_mapping,
            )
            for entity, fields_mapping in source_entities_fields_mapping.items()
        ]
    except KeyError as e:
        raise NonExistingSourceEntityException(f"Source entity {e.args[0]} does not exist")
    return sources


@dataclass
class CompoundEntityFactory:
    def load_entities(self, templates: CompoundEntityTemplates, source_entities: Dict[str, Type]) -> Dict[str, Type]:
        """
        Creates new CompoundEntity types based on provided config.
        Config should contain a valid template that is created according to the schema (see README).

        :param templates: input config containing templates
        :param source_entities: a dictionary with all source Entity types
        :returns: a dictionary with all created CompoundEntity types
        """

        validate_entity_templates(templates)
        return {
            entity_name: self._create_compound_entity(entity_name, entity_schema, source_entities)
            for entity_name, entity_schema in templates.items()
        }

    def _create_compound_entity(
            self, entity_name: str, entity_schema: CompoundEntitySchema, source_entities: Dict[str, Type]
    ) -> Type:
        """
        Creates compound entity of given name according to given schema.
        :param entity_name: new entity name
        :param entity_schema: new entity schema
        :param source_entities: a dictionary with all source Entity types
        :return: new entity type
        """
        source_fields_mapping = create_source_entity_field_mappings(entity_schema)
        sources = create_source_entities(source_entities, source_fields_mapping)

        fields = set()
        fields_with_defaults = set()
        for source in sources:
            for entity_field, source_field in source.fields_mapping.items():
                try:
                    class_field = source.entity.__dataclass_fields__[source_field]
                except KeyError as e:
                    raise SourceEntityFieldException(
                        f"Source entity {source.entity.__name__} field {e.args[0]} does not exist."
                    )
                if isinstance(class_field.default, type(MISSING)):
                    fields.add((entity_field, class_field.type))
                else:
                    fields_with_defaults.add((entity_field, class_field.type, field(default=class_field.default)))

        entity_template = self._create_compound_entity_template(entity_name=entity_name, sources=sources)
        return make_dataclass(
            entity_name,
            list(fields) + list(fields_with_defaults),
            bases=(entity_template,),
            namespace={"__module__": __name__},
        )

    @staticmethod
    def _create_compound_entity_template(entity_name: str, sources: List[SourceEntity]) -> Type:
        return type(
            f"{entity_name}Template",
            (CompoundEntity,),
            {
                "Meta": type(
                    "Meta",
                    (object,),
                    {"sources": sources},
                )
            },
        )
