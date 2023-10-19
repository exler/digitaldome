from typing import Type

from entities.filters import BookFilter, GameFilter, IdentityFilter, MovieFilter, ShowFilter
from entities.forms import BookForm, GameForm, IdentityForm, MovieForm, ShowForm
from entities.models import Book, EntityBase, Game, Identity, Movie, Show

ENTITY_MODEL_TO_FORM_MAPPING = {
    Identity: IdentityForm,
    Movie: MovieForm,
    Show: ShowForm,
    Game: GameForm,
    Book: BookForm,
}

ENTITY_MODEL_TO_FILTER_MAPPING = {
    Identity: IdentityFilter,
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


def get_model_from_entity_type(entity_type: str) -> EntityBase:
    """
    Get model from entity type string, plural or singular.
    """

    model = ENTITY_TYPE_TO_MODEL_MAPPING.get(entity_type, None)
    if model is None:
        raise ValueError(f"Invalid entity type: {entity_type}")

    return model
