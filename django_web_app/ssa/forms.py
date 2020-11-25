from django import forms

class JoinGame(forms.Form):
   game_id = forms.CharField(max_length = 3)

class TestForm(forms.Form):
    #text = forms.CharField(max_length=8, widget=forms.HiddenInput())
    text = forms.CharField(max_length=8, widget=forms.HiddenInput(), initial='valid2')
