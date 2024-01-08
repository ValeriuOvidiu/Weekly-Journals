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
        ('1', 'Weekly Call - Decision Structure "if" / "else"'),
        ('2', 'Weekly Call - Repetitive Structures "while" / "for"'),
        ('3', 'Weekly Call - Number Arrays'),
        ('4', 'Weekly Call - Matrices (Two-Dimensional Arrays)'),
        ('5', 'Weekly Call - Mindset'),
        ('6', 'Weekly Call - Interview Simulations'),
        ('7', 'Weekly Call - Personal Projects')
    ))

class WeeklyJournalModel(models.Model):
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
    journal=models.OneToOneField(WeeklyJournalModel, on_delete=models.CASCADE)  
    