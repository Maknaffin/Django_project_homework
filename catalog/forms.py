from django import forms

from catalog.models import Product, Version
from config.settings import FORBIDDEN_WORDS


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ('owner',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')

        for item in FORBIDDEN_WORDS:
            if item in cleaned_data.lower():
                raise forms.ValidationError('Используются недопустимое название')
        return cleaned_data

    def clean_descriptions(self):
        cleaned_data = self.cleaned_data.get('descriptions')

        for item in FORBIDDEN_WORDS:
            if item in cleaned_data.lower():
                raise forms.ValidationError('Используются недопустимые слова')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


class ModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('name', 'photo', 'price_for_one', 'date_of_creation', 'last_modified_date', 'owner')