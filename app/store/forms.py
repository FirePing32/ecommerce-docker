from django import forms
from store.models import UserDetail, VendorDetail, Item
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'username', 'id':'exampleInputEmail1'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'id':'exampleInputPassword1'}))

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

class UserDetailForm(forms.ModelForm):
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta():
        model = UserDetail
        fields = ('address',)

class VendorForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'username', 'id':'exampleInputEmail1'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'id':'exampleInputPassword1'}))

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

class VendorDetailForm(forms.ModelForm):
    vendordesc = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta():
        model = VendorDetail
        fields = ('vendordesc',)

class ItemForm(forms.ModelForm):
    itemname = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    itemdesc = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    itemprice = forms.IntegerField(required=True, min_value=1, widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta():
        model = Item
        fields = ('itemname', 'itemdesc', 'itemprice')