from datetime import datetime, timedelta
from random import randrange
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from Charts.models import HoursWorkedModel ,WeeklyJurnalModel,CalendarImageModel , Choices
from Charts.forms import userForm, codeForm, loginForm,SaveTime,SearchByDateForm,WeeklyJurnalForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
   


def index(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
    return render(request, "Charts/index.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
    try:
        error = request.session.get("loginError")
        del request.session["loginError"]
        print("cvbnmnbvcvbnvcvb")
    except:
        error = ""
    context = {"form": loginForm, "error": error}

    return render(request, "Charts/login.html", context)


def authentication_code(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
    try:
        error = request.session.get("authenticationCodeError")
        del request.session["authenticationCodeError"]
        print("cvbnmnbvcvbnvcvb")
    except:
        error = ""
    context = {"form": codeForm, "error": error}
    return render(request, "Charts/AuthenticationCode.html", context)


def signUp(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
    try:
        error = request.session.get("authenticateError")
        del request.session["authenticateError"]
        print("cvbnmnbvcvbnvcvb")
    except:
        error = ""
    context = {"form": userForm, "error": error}
    return render(request, "Charts/signUp.html", context)


def authenticate_user(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = userForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                request.session["authenticateError"] = "This email has been used before"
                return redirect("signUp")
            print(email)
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
                print(request.session.get("last_name"))
                request.session.save()
                return redirect("authentication_code")
        request.session["authenticateError"] = "Confirm password faild"
        return redirect("signUp")


def create_user(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")

    if request.method == "POST":
        form = codeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            confirmation_code = request.session.get("confirmation_code")
            print(request.session.get("last_name"))
            print(confirmation_code)
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
                    print(user.username)
                    del request.session["email"]
                    del request.session["password"]
                    del request.session["confirmation_code"]
                    del request.session["first_name"]
                    del request.session["last_name"]
                    login(request, user)
                    return redirect("profile", chartName="hours-worked")

    request.session["authenticationCodeError"] = "introduce the confirmation code again"
    return redirect("authentication_code")


def login_user(request):
    u=request.session.get("u")  
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked"),
    if request.method == "POST":
        form = loginForm(request.POST)  
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
                return redirect("profile", chartName="hours-worked")
            else:
                request.session["loginError"] = "Password incorect"
                return redirect("login_page")


def profile(request, chartName):
    if not request.user.is_authenticated:
        return redirect("login_page")
    print(chartName)
    if "pageName" in request.session:
      del request.session["pageName"] 
    edit= "false" 
    if "edit" in request.session and request.session.get("edit")=="false":  
        edit="true"
     
    request.session["pageName"] = chartName
    request.session.save()
    user = request.user      
    try:
        date = request.session.get("date")
        date_string = date  
        format_string = "%Y-%m-%d"
        date_object = datetime.strptime(date_string, format_string)
        current_date = date_object.date()
        last_monday=current_date - timedelta(days=current_date.weekday())
        print(last_monday,"profile")   
    except:
        date = "null"
        last_monday=datetime.today().date() - timedelta(days=datetime.today().date().weekday())
    try: 
        print(last_monday,user)
        jurnal=WeeklyJurnalModel.objects.get(user=user,date=last_monday)
        select_call_choices=jurnal.select_call.all()
        initial_select_call=[]
        for i in select_call_choices:
            initial_select_call.append(i.description)

        initial_data={"accomplished":jurnal.accomplished,
                      "optional":jurnal.optional,
                      "really_well":jurnal.really_well,
                      "differently":jurnal.differently,
                      "learn":jurnal.learn,
                      "select_call":initial_select_call   
                      }
        print(jurnal.user,jurnal.date)
        calendar_image_model=CalendarImageModel.objects.get(jurnal=jurnal)
        print("a intrat")
        calendar_image=calendar_image_model.calendar.url  
        answers=[jurnal.accomplished,jurnal.optional, jurnal.really_well,jurnal.differently,jurnal.learn,initial_select_call ]


    except: 
       calendar_image="null" 
       initial_data={
                      }
       answers=["","","","","","",]

   
       
    print(calendar_image,"alea")  
    jurnal_labels = [field.label for field in WeeklyJurnalForm()]    
    button_list=[["hours-worked","Worked hours" ],["hours-slept","Slept hours"],["weekly-jurnals","Weekly Jurnals"]]
    context = {"user": user,
               'timeForm':SaveTime,
               'SearchByDate':SearchByDateForm,  
               'date': date,     
               'pageName':chartName,
               'button_list': button_list ,
               'WeeklyJurnalForm': WeeklyJurnalForm(initial=initial_data) ,
               'calendar_image':calendar_image,
               'edit':edit,
             
               'answers':answers,
               "questions":jurnal_labels  
               }  
    return render(request, "Charts/Profile.html", context)

  
  
def logout_user(request):    
    logout(request)
    return redirect("login_page")
