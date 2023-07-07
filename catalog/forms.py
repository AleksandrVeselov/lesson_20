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

        fields = ('title', 'image', 'description', 'category', 'price', 'is_published')  # Выбранные поля
        # exclude = ('image',)  # Кроме поля image

    def clean_title(self):
        """Поиск в названии запрещенных слов и возбуждение ошибки"""
        cleaned_data = self.cleaned_data['title']
        for word in FORBIDDEN_WORDS:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Нельзя добавлять продукты с названием {word}')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_description(self):
        """Поиск в описании запрещенных слов и генерация ошибки"""

        cleaned_data = self.cleaned_data['description']
        for word in FORBIDDEN_WORDS:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Нельзя добавлять продукты у которых в описании есть слово {word}')

        return cleaned_data


class ProductFormModerator(forms.ModelForm):
    """Класс-представление формы для создания продукта для модератора"""

    class Meta:
        model = Product  # Модель, с которой он работает
        fields = ('description', 'category', 'is_published')  # Выбранные поля

    def clean_description(self):
        """Поиск в описании запрещенных слов и генерация ошибки"""

        cleaned_data = self.cleaned_data['description']
        for word in FORBIDDEN_WORDS:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Нельзя добавлять продукты у которых в описании есть слово {word}')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_is_active(self):
        is_active = self.cleaned_data['is_active']
        product = self.cleaned_data['product']
        products = Version.objects.filter(product=product, is_active=True)
        if len(products) != 1:
            print('Нельзя добавить более одной активной версии')
            self.add_error('is_active', 'Нельзя добавить более одной активной версии')
            raise forms.ValidationError('Нельзя добавить более одной активной версии')
        return is_active
