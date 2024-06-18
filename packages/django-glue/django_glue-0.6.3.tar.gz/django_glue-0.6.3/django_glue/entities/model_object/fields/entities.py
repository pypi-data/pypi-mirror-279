from dataclasses import dataclass, field
from typing import Any

from django_glue.entities.model_object.fields.seralizers import serialize_field_value
from django_glue.form.html_attrs import GlueFieldAttrs


@dataclass
class GlueModelField:
    name: str
    type: str
    value: Any
    field_attrs: GlueFieldAttrs

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'value': serialize_field_value(self),
            'field_attrs': self.field_attrs.to_dict(),
        }


@dataclass
class GlueModelFields:
    fields: list[GlueModelField] = field(default_factory=list)

    def __iter__(self):
        return self.fields.__iter__()

    def to_dict(self):
        return {field.name: field.to_dict() for field in self.fields}
