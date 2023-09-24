from datetime import datetime, timedelta
from random import randrange
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from Charts.models import WeeklyJournalModel, CalendarImageModel
from Charts.forms import SaveTime, SearchByDateForm, WeeklyJournalForm
from accounts.forms import UserForm, CodeForm, LoginForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from Charts.views.journals import get_journal_data, get_last_monday


def index(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
    return render(request, "accounts/index.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
    try:
        error = request.session.get("loginError")
        del request.session["loginError"]
    except:
        error = ""
    context = {"form": LoginForm, "error": error}

    return render(request, "accounts/login.html", context)


def authentication_code(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
    try:
        error = request.session.get("authenticationCodeError")
        del request.session["authenticationCodeError"]
       
    except:
        error = ""
    context = {"form": CodeForm, "error": error}
    return render(request, "accounts/AuthenticationCode.html", context)


def signUp_page(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
    try:
        error = request.session.get("authenticateError")
        del request.session["authenticateError"]
       
    except:
        error = ""
    context = {"form": UserForm, "error": error}
    return render(request, "accounts/signUp.html", context)


def authenticate_user(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")
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
                request.session.save()
                return redirect("authentication_code")
        request.session["authenticateError"] = "Confirm password faild"
        return redirect("signUp")


def create_user(request):
    if request.user.is_authenticated:
        return redirect("profile", chartName="hours-worked")

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
                    return redirect("profile", chartName="hours-worked")

    request.session["authenticationCodeError"] = "introduce the confirmation code again"
    return redirect("authentication_code")


def login_user(request):
    if request.user.is_authenticated:
        return (redirect("profile", chartName="hours-worked"),)
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
                return redirect("profile", chartName="hours-worked")
            else:
                request.session["loginError"] = "Password incorect"
                return redirect("login_page")


def profile(request, chartName):
    if not request.user.is_authenticated:
        return redirect("login_page")

    if "pageName" in request.session:
        del request.session["pageName"]

    edit = "false"
    if "edit" in request.session and request.session.get("edit") == "false":
        edit = "true"

    request.session["pageName"] = chartName
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
        "pageName": chartName,
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
