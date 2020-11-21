from django import forms

class JoinGame(forms.Form):
   game_id = forms.CharField(max_length = 3)