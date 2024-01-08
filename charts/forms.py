from django import forms

class DateInputt(forms.DateInput):
    input_type='date'
    

class SaveTime(forms.Form):
    hours=forms.DecimalField(max_digits=5, decimal_places=1,min_value=0,widget=forms.NumberInput(attrs={"class": "form-control"}))      
    date = forms.DateField(widget=DateInputt(attrs={"class": "form-control"})) 
     


class SearchByDateForm(forms.Form):
    date = forms.DateField(widget=DateInputt(attrs={"class": "form-control"}))


class WeeklyJournalForm(forms.Form):
                
     
     accomplished =forms.CharField(required=False,label="1. What have you accomplished this week?", widget=forms.Textarea(attrs={"class": "form-control"}))
     optional=forms.CharField(required=False,label="2. [Optional] How much time did it take for you to solve each problem?",widget=forms.Textarea(attrs={"class": "form-control"}))
     really_well=forms.CharField(required=False,label="3. What went really well? Why?",widget=forms.Textarea(attrs={"class": "form-control"}))
     differently=forms.CharField(label="4. What were some things you could have done differently to move forward faster? \n How exactly could you have done those things?",widget=forms.Textarea(attrs={"class": "form-control"}),required=False)
     learn=forms.CharField(required=False,label="5. What did you learn this week (apart from the lessons)?",widget=forms.Textarea(attrs={"class": "form-control"}))
  
     CHOICES= (
        ('1', 'Weekly Call - Decision Structure "if" / "else"'),
        ('2', 'Weekly Call - Repetitive Structures "while" / "for"'),
        ('3', 'Weekly Call - Number Arrays'),
        ('4', 'Weekly Call - Matrices (Two-Dimensional Arrays)'),
        ('5', 'Weekly Call - Mindset'),
        ('6', 'Weekly Call - Interview Simulations'),
        ('7', 'Weekly Call - Personal Projects')
    ) 
     select_call = forms.MultipleChoiceField(choices=CHOICES,widget=forms.CheckboxSelectMultiple(),label="6. What’s your call attendance this week (specify the date and type of each call you attended to)?",required=False)   
   
    