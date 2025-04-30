from typing import Type

from entities.filters import BookFilter, GameFilter, MovieFilter, ShowFilter
from entities.models import Book, EntityBase, Game, Movie, Show

ENTITY_MODEL_TO_FILTER_MAPPING = {
    Movie: MovieFilter,
    Show: ShowFilter,
    Game: GameFilter,
    Book: BookFilter,
}


def get_entity_type_to_model_mapping() -> dict[str, Type[EntityBase]]:
    mapping = {}
    for subclass in EntityBase.__subclasses__():
        mapping[subclass._meta.verbose_name] = subclass
        mapping[subclass._meta.verbose_name_plural] = subclass

    return mapping


ENTITY_TYPE_TO_MODEL_MAPPING = get_entity_type_to_model_mapping()


def normalize_entity_type(entity_type: str) -> str:
    """
    Get the singular form of the entity type.
    """
    model = ENTITY_TYPE_TO_MODEL_MAPPING.get(entity_type, None)
    if model is None:
        raise ValueError(f"Invalid entity type: {entity_type}")

    return model._meta.verbose_name


def get_model_from_entity_type(entity_type: str) -> EntityBase:
    """
    Get model from entity type string, plural or singular.
    """

    model = ENTITY_TYPE_TO_MODEL_MAPPING.get(entity_type, None)
    if model is None:
        raise ValueError(f"Invalid entity type: {entity_type}")

    return model
