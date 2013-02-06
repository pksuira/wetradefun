from django import forms
 
class ContactForm(forms.Form):
  """ 
  Form for contact
  """
  name = forms.CharField(widget=forms.TextInput(attrs={'class': 'four'}))
  email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'four'}))
  text = forms.CharField(widget=forms.Textarea)