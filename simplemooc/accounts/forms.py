from django import forms
from django.contrib.auth.forms import UserCreationForm
#Como sobrepomos o usuário não podemos mais importar essa classe
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import PasswordReset

from simplemooc.core.mail import send_mail_template
from simplemooc.core.utils import generate_hash_key

#Esta definindo nosso modelo customizado para a classe de usuário
User = get_user_model()

#Esse formulário não está ligado ao model
class PasswordResetForm(forms.Form):
    
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            'Nenhum usuário encontrado com este e-mail'
        )

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save() 
        template_name = 'accounts/password_reset_mail.html'
        subject = 'Criar nova senha no Simple MOOC'
        context = {
            'reset': reset,
        }
        send_mail_template(subject, template_name, context, [user.email])

#Trocado para não criar o form conforme o UserCreationForm, mas somente o ModelForm
class RegisterForm(forms.ModelForm):

    email = forms.EmailField(label = 'E-mail')
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de Senha',
        widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2
    #Removido porque colocamos essa consistência no banco de dados 
    #def clean_email(self):
    #    email = self.cleaned_data['email']
        #Faz a busca no banco do usuário buscando por email e verificando se existe
    #    if User.objects.filter(email=email).exists():
    #        raise forms.ValidationError('Já existe usuário com este e-mail.')
    #    return email


    def save(self, commit=True):
        #sobrepondo o código para o formulário padrão de usuário não commitar as informações no banco
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']

#Essa forma vai pegar os campos do modelo, assim não precisa criar os mesmos no formulário novamente
class EditAccountForm(forms.ModelForm):

    #Removido porque colocamos essa consistência no banco de dados 
    #def clean_email(self):      
        #instance está disponível porque é uma edição   
    #    email = self.cleaned_data['email']
        #Faz a busca no banco do usuário buscando por email, menos o o próprio registro 
    #    queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        # Verifica se existe
    #    if queryset.exists():
    #        raise forms.ValidationError('Já existe usuário com este e-mail.')
    #    return email

    class Meta:
        model = User
        #removido first_name e last_name nosso model atual só têm name
        #fields = ['username', 'email', 'first_name', 'last_name']
        fields = ['username', 'email', 'name']