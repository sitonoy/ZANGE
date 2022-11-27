from django import forms
from .models import ZangeModel,ModelFile
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


class LoginForm(AuthenticationForm):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    for field in self.fields.values():
        field.widget.attrs["class"] = "form-control"
        field.widget.attrs["placeholder"]=field.label

class SignUpForm(UserCreationForm):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    #htmlの表示を変更可能にします
    for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'
        field.widget.attrs['placeholder']=field.label
  class Meta:
    model = User
    fields = ('email','password1','password2')

class InputForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    #htmlの表示を変更可能にします
    for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'
  class Meta:
    model = ZangeModel
    fields = ('date','title','text','url')

class EdinetName(forms.Form):
  name = forms.CharField(
    widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "検索したい企業名",
            'max_length':20,
        }),
  )      

class ImageForm(forms.ModelForm):
   class Meta:
       model = ModelFile
       fields = ('image',)
       