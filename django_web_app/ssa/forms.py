from django import forms
from croppie.fields import CroppieField

from ssa.models import Game


class JoinGame(forms.Form):
   game_id = forms.CharField(max_length = 3)

class TestForm(forms.Form):
    #text = forms.CharField(max_length=8, widget=forms.HiddenInput())
    text = forms.CharField(max_length=8, widget=forms.HiddenInput(), initial='valid2')

class StartGameForm(forms.Form):
    game_id = forms.CharField(max_length=8, widget=forms.HiddenInput())

class AddForm(forms.Form):
    photo = CroppieField(
        options={
            'viewport': {
                'width': 120,
                'height': 140,
            },
            'boundary': {
                'width': 200,
                'height': 220,
            },
            'showZoomer': True,
        },
    )

class CreateGame(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'users', 'owner']
        #fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'test'}),
            'users': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }






