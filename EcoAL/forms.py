from django.forms import ModelForm
from .models import Material as ecoal_Material

class ecoal_MaterialForm(ModelForm):
    class Meta:
        model = ecoal_Material
        fields = [
            'codSinapi', 'ncm', 'description', 'price', 'date'
        ]