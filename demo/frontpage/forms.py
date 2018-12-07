from django import forms
from django.core import validators

class lyricsForModel(forms.Form):
    text = forms.CharField(widget = forms.Textarea)
    
    def clean(self):
        self.fields['text'].label = 'Input your lyrics here:'
        all_clean_data = self.cleaned_data
        #print(all_clean_data.keys())
        
        lyrics = all_clean_data.get('text')
        
        #print(lyrics)
        