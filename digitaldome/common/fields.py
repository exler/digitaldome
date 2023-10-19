from typing import Self

from django.db.models import Model, QuerySet
from django.forms import ValidationError
from django.forms.models import ModelMultipleChoiceField

from digitaldome.common.widgets import ManyToManyWithTextInput


class GetOrCreateManyToManyField(ModelMultipleChoiceField):
    widget = ManyToManyWithTextInput()

    def _check_values(self: Self, value: list[str]) -> QuerySet[Model]:
        """
        Given a list of strings, return a QuerySet of the
        corresponding objects. Raise a ValidationError if a given value is
        invalid (i.e. not a valid value for lookup).
        """
        key = self.to_field_name or "pk"
        # deduplicate given values to avoid creating many querysets or
        # requiring the database backend deduplicate efficiently.
        try:
            value = frozenset(value)
        except TypeError as exc:
            # list of lists isn't hashable, for example
            raise ValidationError(
                self.error_messages["invalid_list"],
                code="invalid_list",
            ) from exc

        model = self.queryset.model

        model.objects.bulk_create(
            [model(**{key: v}) for v in value],
            ignore_conflicts=True,
        )

        return self.queryset.filter(**{f"{key}__in": value}).values_list("id", flat=True)
