from django import forms

from catalog.models import Product, Version

# Запрещенные в названии и в описании слова
FORBIDDEN_WORDS = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')


class ProductForm(forms.ModelForm):
    """Класс-представление формы для создания продукта"""

    class Meta:
        model = Product  # Модель, с которой он работает

        # Поля для заполнения
        # fields = '__all__'  # Все поля
        fields = ('title', 'image', 'description', 'category', 'price')  # Выбранные поля
        # exclude = ('image',)  # Кроме поля image

    def clean_title(self):
        cleaned_data = self.cleaned_data['title']
        for word in FORBIDDEN_WORDS:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Нельзя добавлять продукты с названием {word}')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for word in FORBIDDEN_WORDS:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Нельзя добавлять продукты у которых в описании есть слово {word}')

        return cleaned_data


class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'
