from django.db import models
from django.contrib.auth.models import User

class HoursWorkedModel(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    hours=models.DecimalField(max_digits=5, decimal_places=1)  
    date = models.DateField()


class HoursSleptModel(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    hours=models.DecimalField(max_digits=5, decimal_places=1)  
    date = models.DateField()
    
class Choices(models.Model):
  description = models.CharField(max_length=100,choices=(
        ('1', 'Call săptămânal - Structură de decizie "if" / "else"'),
        ('2', 'Call săptămânal - Structuri repetitive "while" / "for"'),
        ('3', 'Call săptămânal - "Șiruri de numere"'),
        ('4', 'Call săptămânal - "Matrice (Tablouri bidimensionale)"'),
        ('5', 'Call săptămânal - Mindset'),
        ('6', 'Call săptămânal - Simulări de interviuri'),
        ('7', 'Call săptămânal - Proiecte personale')
    ))

class WeeklyJurnalModel(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    accomplished = models.TextField(max_length=255,default="")
    optional = models.TextField(max_length=255,default="")
    really_well = models.TextField(max_length=255,default="")   
    differently = models.TextField(max_length=255,default="")
    learn = models.TextField(max_length=255,default="")
    date = models.DateField()
    select_call = models.ManyToManyField(Choices)
    class Meta:
        unique_together = ('user', 'date') 

class CalendarImageModel(models.Model):
    calendar = models.ImageField(upload_to='Charts/images')
    jurnal=models.OneToOneField(WeeklyJurnalModel, on_delete=models.CASCADE)
    