from django.forms import ModelForm
from .models import Material as sinapi_Material

class sinapi_MaterialForm(ModelForm):
    class Meta:
        model = sinapi_Material
        fields = [
            'codigo', 'nome', 'unidade', 'preco', 'data'
        ]