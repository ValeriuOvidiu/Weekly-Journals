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
('1', 'Call săptămânal - Structură de decizie "if" / "else"'),      
('2', 'Call săptămânal - Structuri repetitive "while" / "for"'),   
('3', 'Call săptămânal - "Șiruri de numere"'),   
('4','Call săptămânal - "Matrice (Tablouri bidimensionale)"'),
('5','Call săptămânal - Mindset'),
('6','Call săptămânal - Simulări de interviuri'),
('7','Call săptămânal - Proiecte personale')  
)  
     select_call = forms.MultipleChoiceField(choices=CHOICES,widget=forms.CheckboxSelectMultiple(),label="6. What’s your call attendance this week (specify the date and type of each call you attended to)?",required=False)   
   
    