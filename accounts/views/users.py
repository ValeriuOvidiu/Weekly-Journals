from datetime import datetime
import json
from random import randrange
from django.http import  JsonResponse
from django.shortcuts import redirect, render    
from django.contrib.auth.models import User
from accounts.models import FriendsRequestModel
from charts.forms import SaveTime, SearchByDateForm, WeeklyJournalForm
from accounts.forms import UserForm, CodeForm, LoginForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from charts.views.journals import get_journal_data, get_last_monday
from django.db.models import Q, Case, When, IntegerField, F, Value



def index(request):
    if request.user.is_authenticated:
        return redirect("profile", chart_name="hours-worked")
    return render(request, "accounts/index.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("profile", chart_name="hours-worked")
    try:
        error = request.session.get("loginError")
        del request.session["loginError"]
    except:
        error = ""
    context = {"form": LoginForm, "error": error}

    return render(request, "accounts/login.html", context)


def authentication_code(request):
    if request.user.is_authenticated:
        return redirect("profile", chart_name="hours-worked")
    try:
        error = request.session.get("authenticationCodeError")
        del request.session["authenticationCodeError"]
       
    except:
        error = ""
    context = {"form": CodeForm, "error": error}  
    return render(request, "accounts/authentication_code.html", context)


def sign_up_page(request):
    if request.user.is_authenticated:
        return redirect("profile", chart_name="hours-worked")
    try:
        error = request.session.get("authenticateError")
        del request.session["authenticateError"]
       
    except:
        error = ""
    context = {"form": UserForm, "error": error}
    return render(request, "accounts/signUp.html", context)


def authenticate_user(request):
    if request.user.is_authenticated:
        return redirect("profile", chart_name="hours-worked")
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                request.session["authenticateError"] = "This email has been used before"
                return redirect("signUp")
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            if password == confirm_password:
                confirmation_code = randrange(1000, 10000)
                send_mail(
                    subject="confirm code ",
                    message="Here is the message:" + str(confirmation_code),
                    from_email="valeriuovidiu1999@gmail.com",
                    recipient_list=[str(email)],
                    fail_silently=False,
                )
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                request.session["email"] = email
                request.session["password"] = password
                request.session["confirmation_code"] = confirmation_code
                request.session["first_name"] = first_name
                request.session["last_name"] = last_name
                confirmation_code = request.session.get("confirmation_code")
                print(confirmation_code)
                request.session.save()
                return redirect("authentication_code")
        request.session["authenticateError"] = "Confirm password faild"
        return redirect("signUp")


def create_user(request):
    if request.user.is_authenticated:
        return redirect("profile", chart_name="hours-worked")

    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            confirmation_code = request.session.get("confirmation_code")
            if code == confirmation_code:
                LastInsertId = -1
                if (User.objects.last()).id:
                    LastInsertId = (User.objects.last()).id
                user = User.objects.create_user(
                    request.session.get("first_name")
                    + " "
                    + request.session.get("last_name")
                    + str(LastInsertId + 1),
                    request.session.get("email"),
                    request.session.get("password"),
                )
                user.first_name = request.session.get("first_name")
                user.last_name = request.session.get("last_name")
                user.save()
                user = authenticate(
                    username=request.session.get("first_name")
                    + " "
                    + request.session.get("last_name")
                    + str(LastInsertId + 1),
                    password=request.session.get("password"),
                )
                if user is not None:
                    del request.session["email"]
                    del request.session["password"]
                    del request.session["confirmation_code"]
                    del request.session["first_name"]
                    del request.session["last_name"]
                    login(request, user)
                    return redirect("profile", chart_name="hours-worked")

    request.session["authenticationCodeError"] = "introduce the confirmation code again"
    return redirect("authentication_code")


def login_user(request):
    if request.user.is_authenticated:
        return (redirect("profile", chart_name="hours-worked"),)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                username = User.objects.get(email=email).username
            except:
                request.session["loginError"] = "Introduce a valid email"
                return redirect("login_page")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile", chart_name="hours-worked")
            else:
                request.session["loginError"] = "Password incorect"
                return redirect("login_page")


def profile(request, chart_name):
    if not request.user.is_authenticated:
        return redirect("login_page")
    if "pageName" in request.session:
        del request.session["pageName"]
    if "visited_user" in request.session:
        del request.session["visited_user"]
    edit = "false"
    if "edit" in request.session and request.session.get("edit") == "false":
        edit = "true"
    request.session["pageName"] = chart_name
    request.session.save()
    user = request.user
    date = request.session.get("date", "null")
    last_monday = get_last_monday(date)
    calendar_image, answers, initial_data = get_journal_data(user, last_monday)
    journal_labels = [field.label for field in WeeklyJournalForm()]
    button_list = [
        ["hours-worked", "Worked hours"],  
        ["hours-slept", "Slept hours"],
        ["weekly-journals", "Weekly Journals"],
    ]

    context = {
        "user": user,
        "timeForm": SaveTime,
        "SearchByDate": SearchByDateForm,
        "date": date,
        "pageName": chart_name,
        "button_list": button_list,
        "WeeklyJurnalForm": WeeklyJournalForm(initial=initial_data),
        "calendar_image": calendar_image,
        "edit": edit,
        "answers": answers,
        "questions": journal_labels,
    }
    return render(request, "accounts/Profile.html", context)


def logout_user(request):
    logout(request)
    return redirect("login_page")


def search_users(request, input_text):
    words = input_text.split()
    column_strings = {
        'first_name': words,
        'last_name': words,
    }  
    result_columns = {}
    for column, strings in column_strings.items():
        virtual_field = Value(0, output_field=IntegerField())
        for word in strings:  
            virtual_field = Case(
                    When(Q(**{f'{column}__istartswith': word}) | Q(**{f'{column}__icontains': " " + word}), then=virtual_field + 2),
                    When(Q(**{f'{column}__icontains': word}), then=virtual_field + 1),
                    default=virtual_field,    
                    output_field=IntegerField(), 
                )
        result_columns[f'{column}_score'] = virtual_field     
  
    results = User.objects.annotate(
        first_name_score=result_columns["first_name_score"],
        last_name_score=result_columns["last_name_score"],
        total=F("first_name_score") + F("last_name_score")
    ).filter(total__gt=0).order_by('-total')

    serialized_results = [{"username": user.username, "first_name": user.first_name, "last_name": user.last_name} for user in results]
    return JsonResponse({"results": serialized_results})

def other_user_profile(request,username,chart_name):
    if not request.user.is_authenticated:
        return redirect("login_page")
    request.session['visited_user']=username
    try:
        other_user = User.objects.get(username=username)
    except:
        return redirect("profile",chart_name="hours-worked")
    friendship_status_json=get_friendship_status(request,username).content.decode('utf-8')
    
    data_dict = json.loads(friendship_status_json)  # Parsați șirul JSON într-un dicționar Python
    value_friendship_status = data_dict.get("friendship_status") 
    friend=False
    if value_friendship_status=="Friends":
        friend=True
    date = request.session.get("date", "null")
    last_monday = get_last_monday(date)
    calendar_image, answers, initial_data = get_journal_data(other_user, last_monday)
    journal_labels = [field.label for field in WeeklyJournalForm()]
    button_list = [
        ["hours-worked", "Worked hours"],
        ["hours-slept", "Slept hours"],
        ["weekly-journals", "Weekly Journals"],
    ]
    user=request.user
    if user==other_user:
        return redirect("profile",chart_name="hours-worked")

    context = {
        "other_user": other_user,
        "user": user,
        "SearchByDate": SearchByDateForm,
        "date": date,
        "pageName": chart_name,
        "button_list": button_list,
        "calendar_image": calendar_image,
        "answers": answers,
        "questions": journal_labels,
        "WeeklyJurnalForm": WeeklyJournalForm(initial=initial_data),
        "friend": friend
    }
    return render(request, "accounts/profile_others.html", context)


def send_friend_requeast(request,username):
    user=request.user
    other_user=User.objects.get(username=username)
    user_is_sender=FriendsRequestModel.objects.filter(sender=user,receiver=other_user)
    other_user_is_sender=FriendsRequestModel.objects.filter(sender=other_user,receiver=user)
    if len(user_is_sender)==0 and len(other_user_is_sender)==0:
        friend_requeast=FriendsRequestModel(sender=user,receiver=other_user,date=datetime.now())
        friend_requeast.save()
    elif len( user_is_sender)==1:  
        user_is_sender[0].delete()
    elif len(other_user_is_sender)==1:
        other_user_is_sender[0].delete()
    return JsonResponse({"succes": 'succes'})

def get_friendship_status(request,username):
    user=request.user
    other_user=User.objects.get(username=username)
    user_is_sender=FriendsRequestModel.objects.filter(sender=user,receiver=other_user)
    other_user_is_sender=FriendsRequestModel.objects.filter(sender=other_user,receiver=user)
    
    if len(user_is_sender)==1 :
        if user_is_sender[0].accepted:
            request.session["friendship_status"]="Friends"
            return JsonResponse({"friendship_status": "Friends"})
        return JsonResponse({"friendship_status": "Cancel the friend request"})
    elif len(other_user_is_sender)==1:
        if other_user_is_sender[0].accepted:
            request.session["friendship_status"]="Friends"
            return JsonResponse({"friendship_status": "Friends"})
        return JsonResponse({"friendship_status": "Accept"})
    else:
        return JsonResponse({"friendship_status": "Add"})   

def friend_request_handler(request,username):  
    user=request.user
    other_user=User.objects.get(username=username)
    user_is_sender=FriendsRequestModel.objects.filter(sender=user,receiver=other_user)
    other_user_is_sender=FriendsRequestModel.objects.filter(sender=other_user,receiver=user)
    if len( user_is_sender)==1:  
        if  user_is_sender[0].accepted:
            user_is_sender[0].delete()
            return redirect ("other_user_profile",username=username,chart_name="hours-worked")
        user_is_sender[0].accepted=True
        user_is_sender[0].date=datetime.now()
        user_is_sender[0].save()
    elif len(other_user_is_sender)==1:
        if  other_user_is_sender[0].accepted:
            other_user_is_sender[0].delete()
            return redirect ("other_user_profile",username=username,chart_name="hours-worked")
        other_user_is_sender[0].accepted=True
        other_user_is_sender[0].date=datetime.now()
        other_user_is_sender[0].save()
    else:
        other_user_is_sender[0].save()
    return redirect ("other_user_profile",username=username,chart_name="hours-worked")


def unread_friend_request(request):
    user=request.user
    unread_notf=(FriendsRequestModel.objects.filter(receiver=user).filter(request_seen=False).filter(accepted=False)|FriendsRequestModel.objects.filter(sender=user).filter(accepted_seen=False).filter(accepted=True)).count()
    return JsonResponse({"unread_notf": unread_notf})  

def friend_request_page(request):
            try:
                user=request.user
                friend_request=(FriendsRequestModel.objects.filter(receiver=user).filter(accepted=False)|FriendsRequestModel.objects.filter(sender=user).filter(accepted_seen=False).filter(accepted=True)).order_by("-id")
                unread_friend_requests=(FriendsRequestModel.objects.filter(receiver=user).filter(request_seen=False).filter(accepted=False)|FriendsRequestModel.objects.filter(sender=user).filter(accepted_seen=False).filter(accepted=True)).count()
                friend_request_list=[{"receiver_first_name": fr_request.receiver.first_name,"receiver_id":fr_request.receiver.id,
                                    "sender_id":fr_request.sender.id,"receiver_username":fr_request.receiver.username,
                                    "sender_username":fr_request.sender.username,  
                                    "receiver_last_name": fr_request.receiver.last_name, "sender_first_name": fr_request.sender.first_name,
                                    "sender_last_name": fr_request.sender.last_name,"date":fr_request.date.strftime('%Y-%m-%d %H:%M')} for fr_request in friend_request]
                for rows in friend_request:
                    if rows.sender==user:
                        rows.accepted_seen=True
                        rows.save()
                    else:
                        rows.request_seen=True
                        rows.save()
            
            except:
                friend_request_list=None
                unread_friend_requests=0
            context={
               'friend_request' :friend_request_list,    
               'unread_friend_requests':unread_friend_requests
            }
            return render(request, "accounts/friend_requests.html", context)
