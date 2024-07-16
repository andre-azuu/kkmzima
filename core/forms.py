from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Farmer, Consumer, eggInventory, Farm, expenseInventory

class ExpenseInventoryForm(forms.ModelForm):
    class Meta:
        model = expenseInventory
        fields = [ 'particulars', 'quantity', 'unitPrice']

class eggInventoryForm(forms.ModelForm):
    class Meta:
        model = eggInventory
        fields = ['stock', 'trayPrice', 'batch_number']

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = [ 'name', 'location']

class FarmerSignUpForm(UserCreationForm):
    farmerPhone = forms.CharField(max_length=15, required=False)
    farmerEmail = forms.EmailField(max_length=100, required=False)
    farmerAddress = forms.CharField(max_length=100, required=False)


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_farmer = True
        if commit:
            user.save()
            Farmer.objects.create(user=user, farmerUsername=user.username,
                farmerPhone=self.cleaned_data.get('farmerPhone', ''),
                farmerEmail=self.cleaned_data.get('farmerEmail', ''),
                farmerAddress=self.cleaned_data.get('farmerAddress', '')
            )
        return user

class ConsumerSignUpForm(UserCreationForm):
    consumerPhone = forms.CharField(max_length=15)
    consumerAddress = forms.CharField(max_length=100, required=False)
    consumerEmail = forms.EmailField(max_length=100,  required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_consumer = True
        if commit:
            user.save()
            Consumer.objects.create(
                user=user, 
                consumerUsername=user.username,
                consumerPhone=self.cleaned_data.get('consumerPhone', ''),
                consumerAddress=self.cleaned_data.get('consumerAddress', ''),
                consumerEmail= self.cleaned_data.get(' consumerEmail',''),
                )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
