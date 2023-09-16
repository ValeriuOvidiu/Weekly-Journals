from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from Charts.models import (
    HoursWorkedModel,
    HoursSleptModel,
    WeeklyJurnalModel,
    CalendarImageModel,
    Choices,
)
from django.contrib.auth.models import User
from django.http import JsonResponse
from Charts.forms import SaveTime, SearchByDateForm, WeeklyJurnalForm


def upload_jurnal(request):
    if request.method == "POST":
        form = WeeklyJurnalForm(request.POST)
        if form.is_valid():
            accomplished = form.cleaned_data["accomplished"]
            optional = form.cleaned_data["optional"]
            really_well = form.cleaned_data["really_well"]
            differently = form.cleaned_data["differently"]
            learn = form.cleaned_data["learn"]
            select_call = form.cleaned_data["select_call"]
            print(select_call)
            user = request.user
            try:
                date = request.session.get("date")
                date_string = date
                format_string = "%Y-%m-%d"
                date_object = datetime.strptime(date_string, format_string)
                current_date = date_object.date()
                last_monday = current_date - timedelta(days=current_date.weekday())
                print(last_monday, "cur")
            except:
                last_monday = datetime.today().date() - timedelta(
                    days=datetime.today().date().weekday()
                )
            try:
                jurnal_model = WeeklyJurnalModel.objects.get(
                    user=user, date=last_monday
                )
                jurnal_model.accomplished = accomplished
                jurnal_model.optional = optional
                jurnal_model.really_well = really_well
                jurnal_model.differently = differently
                jurnal_model.learn = learn
                jurnal_model.save()
                choices = Choices.objects.all()
                for i in select_call:
                    for j in choices:
                        print(j)
                        if j.description == i:
                            print("ce faci")
                            jurnal_model.select_call.add(j)
                            jurnal_model.save()

            except:
                jurnal_model = WeeklyJurnalModel(
                    user=user,
                    date=last_monday,
                    accomplished=accomplished,
                    optional=optional,
                    really_well=really_well,
                    differently=differently,
                    learn=learn,
                    select_call=select_call,
                )
                jurnal_model.save()
            return redirect("edit")


def upload_calendar_image(request):
    if request.method == "POST":
        calendar_image = request.FILES.get("file")
        user = request.user
        try:
            date = request.session.get("date")
            date_string = date
            format_string = "%Y-%m-%d"
            date_object = datetime.strptime(date_string, format_string)
            current_date = date_object.date()
            last_monday = current_date - timedelta(days=current_date.weekday())
        except:
            last_monday = datetime.today().date() - timedelta(
                days=datetime.today().date().weekday()
            )
        try:
            jurnal_model = WeeklyJurnalModel.objects.get(user=user, date=last_monday)
            calendar_image_model = CalendarImageModel.objects.get(jurnal=jurnal_model)
            calendar_image_model.calendar = calendar_image
            calendar_image_model.save()

        except:
            jurnal_model = WeeklyJurnalModel(user=user, date=last_monday)
            jurnal_model.save()
            calendar_image_model = CalendarImageModel(
                calendar=calendar_image, jurnal=jurnal_model
            )
            calendar_image_model.save()

        return redirect("profile", chartName="weekly-jurnals")


def edit_jurnal(request):
    if "edit" in request.session and request.session.get("edit") == "false":
        request.session["edit"] = "true"
    else:
        request.session["edit"] = "false"

    return redirect("profile", chartName="weekly-jurnals")
