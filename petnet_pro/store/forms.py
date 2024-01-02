from django import forms
from .models import Product

# form for our products list with props
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image',)
        widgets = {
            'category':forms.Select(attrs={
                'class':'mb-2 p-4 border border-blue-300'
            }),
            'title':forms.TextInput(attrs={
                'class':'mb-2 p-2 border-2 border-blue-300'
            }
            ),
            'description':forms.Textarea(
                attrs={
                'class':'mb-2 p-2 border-2 border-blue-300'
            }
            ),
            'price':forms.NumberInput(attrs={
                'class':'mb-2 p-2 border-2 border-blue-300'
            }
            ),
            

        }
