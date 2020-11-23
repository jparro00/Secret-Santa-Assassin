from django import forms

class JoinGame(forms.Form):
   game_id = forms.CharField(max_length = 3)

class TestForm(forms.Form):
    post = forms.CharField(max_length=8)