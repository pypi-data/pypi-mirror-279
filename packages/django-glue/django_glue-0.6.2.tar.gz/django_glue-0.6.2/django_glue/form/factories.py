from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Union, Any

from django.db.models import Field

from django_glue.form.enums import GlueAttrType
from django_glue.form.html_attrs import GlueFieldAttrs, GlueFieldAttr


class GlueAttrFactory(ABC):

    def __init__(self, model_field: Field):
        self.model_field = model_field
        self.glue_field_attrs = GlueFieldAttrs()

    def add_attr(
            self,
            name: str,
            value: Any,
            attr_type: GlueAttrType
    ) -> None:
        attr = GlueFieldAttr(name=name, value=value, attr_type=attr_type)
        self.glue_field_attrs += attr

    @abstractmethod
    def add_field_attrs(self):
        pass

    def add_base_attrs(self):
        self.add_attr('name', self.model_field.name, GlueAttrType.HTML)
        self.add_attr('id', f'id_{self.model_field.name}', GlueAttrType.HTML)
        self.add_attr('label', str(self.model_field.verbose_name).title(), GlueAttrType.FIELD)

        if not self.model_field.blank:
            self.add_attr('required', True, GlueAttrType.HTML)

        # Todo: Need to deal with hidden. The label shouldn't show if it is hidden...
        # if self.model_field.hidden:
        #     self.add_attr('hidden', True, GlueAttrType.HTML)

        if self.model_field.max_length:
            self.add_attr('maxlength', self.model_field.max_length, GlueAttrType.HTML)

        if self.model_field.help_text:
            self.add_attr('help_text', str(self.model_field.help_text), GlueAttrType.FIELD)

        if self.model_field.choices:
            self.add_attr('choices', self.model_field.choices, GlueAttrType.FIELD)

    def factory_method(self) -> GlueFieldAttrs:
        self.glue_field_attrs = GlueFieldAttrs()
        self.add_base_attrs()
        self.add_field_attrs()
        return self.glue_field_attrs


class GlueBooleanAttrFactory(GlueAttrFactory):
    def add_field_attrs(self):
        bool_choices = [
            (True, 'Yes'),
            (False, 'No')
        ]
        self.add_attr('choices', bool_choices, GlueAttrType.FIELD)


class GlueCharAttrFactory(GlueAttrFactory):
    def add_field_attrs(self):
        pass


class GlueDateAttrFactory(GlueAttrFactory):
    def add_field_attrs(self):
        self.add_attr('max', '', GlueAttrType.HTML)
        self.add_attr('min', '', GlueAttrType.HTML)


class GlueTextAreaAttrFactory(GlueAttrFactory):
    def add_field_attrs(self):
        self.add_attr('cols', 20, GlueAttrType.HTML)
        self.add_attr('rows', 3, GlueAttrType.HTML)

        if self.model_field.max_length:
            self.add_attr('maxlength', self.model_field.max_length, GlueAttrType.HTML)


class GlueIntegerAttrFactory(GlueTextAreaAttrFactory):
    def add_field_attrs(self):
        self.max_min_validation_attr()
        self.step_attr()

    def max_min_validation_attr(self):
        valid_range = range(-999999999, 999999999)  # This is an arbitrary number. Django default creates errors.
        max_min_validators = ['min_value', 'max_value']
        for validator in self.model_field.validators:

            if hasattr(validator, 'code') and validator.code in max_min_validators:

                if validator.limit_value in valid_range:
                    self.add_attr(validator.code.split('_')[0], validator.limit_value, GlueAttrType.HTML)
                else:
                    self.add_attr(validator.code.split('_')[0], None, GlueAttrType.HTML)

    def step_attr(self):
        self.add_attr('step', 1, GlueAttrType.HTML)


class GlueDecimalAttrFactory(GlueIntegerAttrFactory):
    def add_field_attrs(self):
        super().add_field_attrs()

    def step_attr(self):
        validator = next((v for v in self.model_field.validators if hasattr(v, 'decimal_places')), None)

        if validator:
            step_value = Decimal('1') / (10 ** validator.decimal_places)
            self.add_attr('step', float(step_value), GlueAttrType.HTML)
        else:
            self.add_attr('step', 0.01, GlueAttrType.HTML)



