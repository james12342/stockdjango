from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *

class AdsForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'title', 
        'placeholder': 'Title'
    }))

    description = forms.CharField(widget=CKEditorWidget(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'description', 
        'placeholder': 'Description'
    }))

    price = forms.CharField(widget=forms.NumberInput(attrs={
        'class': 'form-control',  
        'name': 'price', 
        'placeholder': 'Price'
    }))

    country = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'country', 
        'placeholder': 'country'
    }))

    state = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'state', 
        'placeholder': 'state'
    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'city', 
        'placeholder': 'City'
    }))

    category = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'category', 
        'placeholder': 'category'
    }))

    condition = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'condition', 
        'placeholder': 'condition'
    }))

    postJavascript = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'postJavascript', 
        'placeholder': 'postJavascript'
    }))

    postImageUrl = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'postImageUrl', 
        'placeholder': 'postImageUrl'
    }))

    postADUrl = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'postADUrl', 
        'placeholder': 'postADUrl'
    }))

    postADClickCount = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'postADClickCount', 
        'placeholder': 'postADClickCount'
    }))
    postADClickPerEarn = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'postADClickPerEarn', 
        'placeholder': 'postADClickPerEarn'
    }))
    postADTotalEarn = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'postADTotalEarn', 
        'placeholder': 'postADTotalEarn'
    }))
    postIPaddress = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'postIPaddress', 
        'placeholder': 'postIPaddress'
    }))
    postADViewerIP = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'postADViewerIP', 
        'placeholder': 'postADViewerIP'
    }))
    video = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'video', 
        'placeholder': 'video'
    }))
    is_featured = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'is_featured', 
        'placeholder': 'is_featured'
    }))
    is_active = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'is_active', 
        'placeholder': 'is_active'
    }))
    brand = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'brand', 
        'placeholder': 'Brand'
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'phone', 
        'placeholder': 'Phone'
    }))

    class Meta:
        model = Ads
        fields = '__all__'
        exclude = ['author', 'date_created', 'is_featured']

    

    
        