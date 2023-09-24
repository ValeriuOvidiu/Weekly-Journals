from django import forms


class UserForm(forms.Form):
    first_name = forms.CharField( min_length=1,widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'Enter your first name'}))  
    last_name = forms.CharField( min_length=1,widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'Enter your last name'}) ) 
    email = forms.EmailField(min_length=1,widget=forms.EmailInput(attrs={"class": "form-control",'placeholder': 'Enter your email'}))
    password = forms.CharField(
         widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Choose a password'}), min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Confirm the password'}), min_length=6  
    )


class CodeForm(forms.Form):
    code = forms.IntegerField(
        help_text="introduce text", max_value=9999, min_value=1000 , widget=forms.PasswordInput(attrs={"class": "form-control"}))
    
   
class LoginForm(forms.Form):
    email= forms.EmailField(min_length=1,widget=forms.EmailInput(attrs={"class": "form-control",'placeholder': 'Enter your email'}))
    password = forms.CharField(
         widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Choose a password'}), min_length=6
    )