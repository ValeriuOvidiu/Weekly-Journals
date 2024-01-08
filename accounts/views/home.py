from django.shortcuts import  render    
from django.contrib.auth.models import User
from django.db.models import Sum

def get_top():
    top_workers=User.objects.annotate(total_worked_hours=Sum('hoursworkedmodel__hours')).filter(total_worked_hours__gt=0).order_by('-total_worked_hours')
    top_sleepers=User.objects.annotate(total_slept_hours=Sum('hourssleptmodel__hours')).filter(total_slept_hours__gt=0).order_by('-total_slept_hours')
    serialized_top_workers_results = [{"index": index, "total_worked_hours": user.total_worked_hours, 'username': user.username, "first_name": user.first_name, "last_name": user.last_name} for index, user in enumerate(top_workers, start=1)]
    serialized_top_sleepers_results = [{"index": index, "total_slept_hours": user.total_slept_hours, 'username': user.username, "first_name": user.first_name, "last_name": user.last_name} for index, user in enumerate(top_sleepers, start=1)]
    return serialized_top_workers_results,serialized_top_sleepers_results


def home(request):   
    serialized_top_workers_results,serialized_top_sleepers_results=get_top()
    context={'serialized_top_workers_results':serialized_top_workers_results,
             'serialized_top_sleepers_results':serialized_top_sleepers_results
             }
    return render(request, "accounts/home.html",context)