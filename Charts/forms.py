from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.core.exceptions import ValidationError
from Charts.models import WeeklyJurnalModel
from datetime import datetime, timedelta



class userForm(forms.Form):
    first_name = forms.CharField( min_length=1,widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'Enter your first name'}))  
    last_name = forms.CharField( min_length=1,widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'Enter your last name'}) ) 
    email = forms.EmailField(min_length=1,widget=forms.EmailInput(attrs={"class": "form-control",'placeholder': 'Enter your email'}))
    password = forms.CharField(
         widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Choose a password'}), min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Confirm the password'}), min_length=6  
    )


class codeForm(forms.Form):
    code = forms.IntegerField(
        help_text="introduce text", max_value=9999, min_value=1000 , widget=forms.PasswordInput(attrs={"class": "form-control"}))
    


class DateInputt(forms.DateInput):
    input_type='date'

   
class loginForm(forms.Form):
    email= forms.EmailField(min_length=1,widget=forms.EmailInput(attrs={"class": "form-control",'placeholder': 'Enter your email'}))
    password = forms.CharField(
         widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Choose a password'}), min_length=6
    )
    


class SaveTime(forms.Form):
    hours=forms.DecimalField(max_digits=5, decimal_places=1,min_value=0,widget=forms.NumberInput(attrs={"class": "form-control"}))      
    date = forms.DateField(widget=DateInputt(attrs={"class": "form-control"})) 
     


class SearchByDateForm(forms.Form):
    date = forms.DateField(widget=DateInputt(attrs={"class": "form-control"}))


class WeeklyJurnalForm(forms.Form):
                
     
     accomplished =forms.CharField(required=False,label="1. What have you accomplished this week?", widget=forms.Textarea(attrs={"class": "form-control"}))
     optional=forms.CharField(required=False,label="2. [Optional] How much time did it take for you to solve each problem?",widget=forms.Textarea(attrs={"class": "form-control"}))
     really_well=forms.CharField(required=False,label="3. What went really well? Why?",widget=forms.Textarea(attrs={"class": "form-control"}))
     differently=forms.CharField(label="4. What were some things you could have done differently to move forward faster? \n How exactly could you have done those things?",widget=forms.Textarea(attrs={"class": "form-control"}),required=False)
     learn=forms.CharField(required=False,label="5. What did you learn this week (apart from the lessons)?",widget=forms.Textarea(attrs={"class": "form-control"}))
  
     CHOICES= (  
('1', 'Call săptămânal - Structură de decizie "if" / "else"'),      
('2', 'Call săptămânal - Structuri repetitive "while" / "for"'),   
('3', 'Call săptămânal - "Șiruri de numere"'),   
('4','Call săptămânal - "Matrice (Tablouri bidimensionale)"'),
('5','Call săptămânal - Mindset'),
('6','Call săptămânal - Simulări de interviuri'),
('7','Call săptămânal - Proiecte personale')  
)  
     select_call = forms.MultipleChoiceField(choices=CHOICES,widget=forms.CheckboxSelectMultiple(),label="6. What’s your call attendance this week (specify the date and type of each call you attended to)?",required=False)   
   
    