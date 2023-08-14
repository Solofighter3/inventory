from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Contact,YourItem,Orders
from django import forms
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username',"email",'password1','password2', )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['email','desc']

        
class Itemfield(ModelForm):
    class Meta:
        model=YourItem
        fields=['name','cost_per_item','ammount_in_stock','ammount_sold']

class Orderform(ModelForm):
    class Meta:
        model=Orders
        fields=['ordername','Orderer_Username','orderer_phoneno','order_location','product_ordered']