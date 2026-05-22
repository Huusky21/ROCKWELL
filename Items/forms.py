from django import forms

from .models import Accesorio, Huacal, Registro, SOItem


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


class HuacalSelectField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        tipo = obj.get_tipo_display().rstrip('s')
        desc = f' — {obj.descripcion}' if obj.descripcion else ''
        return f'{obj.pn} ({tipo}){desc}'


class AccesorioAutoCreateField(forms.CharField):
    def to_python(self, value):
        if not value:
            return None
        codigo = str(value).strip()
        if not codigo:
            return None
        accesorio, _ = Accesorio.objects.get_or_create(codigo=codigo)
        return accesorio


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
    huacal = HuacalSelectField(
        queryset=Huacal.objects.filter(activo=True).order_by('tipo', 'pn'),
        required=False,
        empty_label='— Sin huacal —',
    )
    accesorio = AccesorioAutoCreateField(
        required=False,
        widget=forms.TextInput(attrs={
            'list': 'accesorios',
            'autocomplete': 'off',
            'placeholder': 'Código del accesorio (se crea si no existe)',
        }),
    )

    class Meta(RegistroForm.Meta):
        fields = ['so_item', 'cantidad']
