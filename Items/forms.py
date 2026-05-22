from django import forms

from .models import Huacal, Registro, SOItem


class SOItemComboboxField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, SOItem):
            return value
        try:
            return super().to_python(value)
        except forms.ValidationError:
            text_value = str(value).strip()
            if ' (' in text_value:
                text_value = text_value.split(' (', 1)[0]
            try:
                return self.queryset.get(so_item=text_value)
            except SOItem.DoesNotExist:
                raise forms.ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')


class HuacalComboboxField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        tipo = obj.get_tipo_display().rstrip('s')
        desc = f' — {obj.descripcion}' if obj.descripcion else ''
        return f'{obj.pn} ({tipo}){desc}'

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, Huacal):
            return value
        text = str(value).strip()
        if not text:
            return None
        pn = text.split(' (', 1)[0].strip()
        try:
            return self.queryset.get(pn=pn)
        except Huacal.DoesNotExist:
            raise forms.ValidationError(
                'Huacal no encontrado. Crea uno nuevo desde la sección de abajo.',
            )


class RegistroForm(forms.ModelForm):
    so_item = SOItemComboboxField(
        queryset=SOItem.objects.all(),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'so_items',
            'autocomplete': 'off',
            'placeholder': 'Seleccione o escriba un SO Item',
        }),
    )

    class Meta:
        model = Registro
        fields = ['so_item', 'cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class CapturarForm(RegistroForm):
    huacal = HuacalComboboxField(
        queryset=Huacal.objects.filter(activo=True).order_by('tipo', 'pn'),
        to_field_name='pn',
        required=False,
        widget=forms.TextInput(attrs={
            'list': 'huacales',
            'autocomplete': 'off',
            'placeholder': 'Selecciona o escribe un PN (ej. PN-48336)',
        }),
    )

    class Meta(RegistroForm.Meta):
        fields = ['so_item', 'cantidad']
