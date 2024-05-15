from django import forms
from .models import AgendarEvento, Artista, Estado, Pagamentos


class AgendarEventoForms(forms.ModelForm):

    class Meta:
        model = AgendarEvento
        fields = '__all__'
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control', 'id': 'id_estado'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uf'].required = False
        self.fields['cidade'].required = False
        self.fields['status'].required = False
        self.fields['producao'].required = False
        self.fields['comissao'].required = False
        self.fields['nome_vendedor'].required = False
        self.fields['data_enviado'].required = False
        self.fields['data_assinado'].required = False
        self.fields['diaria'].required = False
        self.fields['valor_diaria'].required = False
        self.fields['contato_nome_tel'].required = False
        self.fields['custos'].required = False
        self.fields['operacional'].required = False
        self.fields['obs'].required = False
        self.fields['estado'].queryset = Estado.objects.all()

        if 'uf' in self.initial:
            self.fields['uf'].initial = self.initial['uf']
        if 'cidade' in self.initial:
            self.fields['cidade'].initial = self.initial['cidade']

class ArtistaForm(forms.ModelForm):

    class Meta:
        model = Artista
        fields = '__all__'


class PagamentosForms(forms.ModelForm):

    class Meta:
        model = Pagamentos
        exclude = ['evento']

# class FiltroForm(forms.Form):
#     cidade = forms.CharField(label='Cidade', required=False)
#     vendedor = forms.CharField(label='Vendedor', required=False)
#     ano = forms.IntegerField(label='Ano', required=False)
#     mes = forms.ChoiceField(choices=[(i, f"{i:02d}") for i in range(1, 13)], label='Mês', required=False)
#     status = forms.CharField(label='Status', required=False)
#     artista = forms.CharField(label='Artista', required=False)