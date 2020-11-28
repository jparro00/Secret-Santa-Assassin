from django import forms

from ssa.models import Game


class JoinGame(forms.Form):
   game_id = forms.CharField(max_length = 3)

class TestForm(forms.Form):
    #text = forms.CharField(max_length=8, widget=forms.HiddenInput())
    text = forms.CharField(max_length=8, widget=forms.HiddenInput(), initial='valid2')

class StartGameForm(forms.Form):
    game_id = forms.CharField(max_length=8, widget=forms.HiddenInput())


class CreateGame(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'users', 'owner']
        #fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'users': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }






