from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from charts.models import (
    HoursWorkedModel,
    HoursSleptModel,
    WeeklyJournalModel,
    CalendarImageModel,
    Choices,
)

from django.contrib.auth.models import User
from django.http import JsonResponse
from charts.forms import SaveTime, SearchByDateForm, WeeklyJournalForm


def upload_journal(request):
    if request.method == "POST":
        form = WeeklyJournalForm(request.POST)
        if form.is_valid():
            accomplished = form.cleaned_data["accomplished"]
            optional = form.cleaned_data["optional"]
            really_well = form.cleaned_data["really_well"]
            differently = form.cleaned_data["differently"]
            learn = form.cleaned_data["learn"]
            select_call = form.cleaned_data["select_call"]
            print(select_call)
            user = request.user
            date = request.session.get("date", "null")
            last_monday = get_last_monday(date)
            try:
                journal_model = WeeklyJournalModel.objects.get(
                    user=user, date=last_monday
                )
                journal_model.accomplished = accomplished
                journal_model.optional = optional
                journal_model.really_well = really_well
                journal_model.differently = differently
                journal_model.learn = learn
                journal_model.save()
                journal_model.select_call.clear()
                choices = Choices.objects.all()
                for i in select_call:
                    for j in choices:
                        print(j)
                        if j.description == i:
                            print("ce faci")
                            journal_model.select_call.add(j)
                            journal_model.save()

            except:
                journal_model = WeeklyJournalModel(
                    user=user,
                    date=last_monday,
                    accomplished=accomplished,
                    optional=optional,
                    really_well=really_well,
                    differently=differently,
                    learn=learn,
                )
                journal_model.save()
                choices = Choices.objects.all()
                for i in select_call:
                    for j in choices:
                        print(j)
                        if j.description == i:
                            print("ce faci")
                            journal_model.select_call.add(j)
                            journal_model.save()

            return redirect("edit")


def upload_calendar_image(request):
    if request.method == "POST":
        calendar_image = request.FILES.get("file")
        user = request.user
        date = request.session.get("date", "null")
        last_monday = get_last_monday(date)
        try:
            journal_model = WeeklyJournalModel.objects.get(user=user, date=last_monday)
            try:
                calendar_image_model = CalendarImageModel.objects.get(
                    journal=journal_model
                )
                calendar_image_model.calendar = calendar_image
                calendar_image_model.save()
            except:
                calendar_image_model = CalendarImageModel(
                    calendar=calendar_image, journal=journal_model
                )
                calendar_image_model.save()

        except:
            journal_model = WeeklyJournalModel(user=user, date=last_monday)
            journal_model.save()
            calendar_image_model = CalendarImageModel(
                calendar=calendar_image, journal=journal_model
            )
            calendar_image_model.save()
            print("e treaba")

        return redirect("profile", chart_name="weekly-journals")


def edit_journal(request):
    print("edit este gasit")
    if "edit" in request.session and request.session.get("edit") == "false": 
        request.session["edit"] = "true"
    else:
        request.session["edit"] = "false"

    return redirect("profile", chart_name="weekly-journals")


def get_journal_data(user, last_monday):
    try:
        journal = WeeklyJournalModel.objects.get(user=user, date=last_monday)
        select_call_choices = journal.select_call.all()
        initial_select_call = [i.description for i in select_call_choices]

        initial_data = {
            "accomplished": journal.accomplished,
            "optional": journal.optional,
            "really_well": journal.really_well,
            "differently": journal.differently,
            "learn": journal.learn,
            "select_call": initial_select_call,
        }
        try:
            calendar_image_model = CalendarImageModel.objects.get(journal=journal)
            calendar_image = calendar_image_model.calendar.url
        except:
            calendar_image = "null"
        answers = [
            journal.accomplished,
            journal.optional,
            journal.really_well,
            journal.differently,
            journal.learn,
            initial_select_call,
        ]
    except:
        calendar_image = "null"
        initial_data = {}
        answers = ["", "", "", "", "", ""]
    return calendar_image, answers, initial_data


def get_last_monday(date_string):
    try:
        format_string = "%Y-%m-%d"
        date_object = datetime.strptime(date_string, format_string)
        current_date = date_object.date()
        last_monday = current_date - timedelta(days=current_date.weekday())
        return last_monday
    except:
        return datetime.today().date() - timedelta(
            days=datetime.today().date().weekday()
        )
