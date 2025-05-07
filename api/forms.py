# api/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User # Django'нун демейки User модели

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True, # Email'ди милдеттүү кылабыз
        help_text='Милдеттүү. Жарактуу email дарегин киргизиңиз.'
    )
    first_name = forms.CharField(
        max_length=30,
        required=False, # Аты-жөнү милдеттүү эмес (каалооңузга жараша)
        help_text='Милдеттүү эмес.'
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        help_text='Милдеттүү эмес.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # UserCreationForm демейки боюнча 'username' талаасын камтыйт.
        # Ага биз кошкон 'email', 'first_name', 'last_name' талааларын кошобуз.
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    # Эгер username'ди email менен бирдей кылгыңыз келсе, же башка логика болсо,
    # save() методун кайра аныктасаңыз болот.
    # Мисалы, эгер username'ди email'ден автоматтык түрдө алгыңыз келсе:
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.username = self.cleaned_data['email'].split('@')[0] # Же башка уникалдуу логика
    #     if commit:
    #         user.save()
    #     return user