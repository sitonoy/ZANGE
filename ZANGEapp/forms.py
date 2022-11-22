from django import forms
from .models import ZangeModel
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


class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self):
        subject = "お問い合わせ"
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]  # 受信者リスト
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")

class EdinetName(forms.Form):
  name = forms.CharField(
    widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "検索したい企業名",
            'max_length':20,
        }),
  )      