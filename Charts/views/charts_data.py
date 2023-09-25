from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from charts.models import HoursWorkedModel, HoursSleptModel
from django.contrib.auth.models import User
from charts.forms import SaveTime, SearchByDateForm  



class WorkedChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, username, searched_date):  # Use the get method
        try:
            user = User.objects.get(username=username)
        except:
            user = request.user

        if searched_date != "null":
            date_string = searched_date
            format_string = "%Y-%m-%d"
            date_object = datetime.strptime(date_string, format_string)

            current_date = date_object.date()
        else:
            current_date = datetime.today().date()

        num_of_mondays = 14
        today = current_date
        weekday = today.weekday()
        last_monday = today - timedelta(days=weekday)
        mondays = [
            last_monday - timedelta(weeks=week) for week in range(num_of_mondays)
        ]
        reversed_mondays = list(reversed(mondays))

        last_100_days = [current_date - timedelta(days=i) for i in range(100)]
        reversed_last_100_days = list(reversed(last_100_days))
        daily_charts_data = [[0 for _ in range(100)] for _ in range(2)]
        i = 0

        for dates in reversed_last_100_days:
            try:
                check_date = HoursWorkedModel.objects.get(user=user, date=dates)
                daily_charts_data[0][i] = dates
                daily_charts_data[1][i] = check_date.hours

            except:
                daily_charts_data[0][i] = dates
                daily_charts_data[1][i] = 0

            i += 1
        i = 99
        j = 0
        week_total = 0
        week_charts_data = [[0 for _ in range(14)] for _ in range(2)]
        for dates in last_100_days:
            week_total += daily_charts_data[1][i]
            if j < 14 and dates == mondays[j]:
                week_charts_data[0][j] = mondays[j]
                week_charts_data[1][j] = week_total
                week_total = 0
                j += 1
            i -= 1
        week_charts_data[0] = list(reversed(week_charts_data[0]))
        week_charts_data[1] = list(reversed(week_charts_data[1]))

        charts_data = [daily_charts_data, week_charts_data]

        return Response(charts_data)


def worked_hours_save(request):
    user = request.user
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SaveTime(request.POST)
        # check whether it's valid:
        if form.is_valid():
            date = form.cleaned_data["date"]
            hours = form.cleaned_data["hours"]
            try:
                check_date = HoursWorkedModel.objects.get(user=user, date=date)
                check_date.hours = hours
                check_date.save()

            except:
                hours_worked = HoursWorkedModel(user=user, hours=hours, date=date)
                hours_worked.save()
            return redirect("profile", chartName="hours-worked")


def search_by_date(request, chartName):
    if request.method == "POST":
        form = SearchByDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            date_string = date.strftime("%Y-%m-%d")  # Convert datetime.date to string
            request.session["date"] = date_string
            return redirect("profile", chartName=chartName)


class SleptChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, username, searched_date):  # Use the get method
        try:
            user = User.objects.get(username=username)
        except:
            user = request.user

        if searched_date != "null":
            date_string = searched_date
            format_string = "%Y-%m-%d"
            date_object = datetime.strptime(date_string, format_string)

            current_date = date_object.date()
        else:
            current_date = datetime.today().date()

        num_of_mondays = 14
        today = current_date
        weekday = today.weekday()
        last_monday = today - timedelta(days=weekday)
        mondays = [
            last_monday - timedelta(weeks=week) for week in range(num_of_mondays)
        ]
        reversed_mondays = list(reversed(mondays))

        last_100_days = [current_date - timedelta(days=i) for i in range(100)]
        reversed_last_100_days = list(reversed(last_100_days))
        print(reversed_mondays)
        print(reversed_last_100_days)
        daily_charts_data = [[0 for _ in range(100)] for _ in range(2)]
        i = 0
        print(user)
        for dates in reversed_last_100_days:
            try:
                check_date = HoursSleptModel.objects.get(user=user, date=dates)
                daily_charts_data[0][i] = dates
                daily_charts_data[1][i] = check_date.hours

            except:
                daily_charts_data[0][i] = dates
                daily_charts_data[1][i] = 0

            i += 1
        i = 99
        j = 0
        week_total = 0
        week_charts_data = [[0 for _ in range(14)] for _ in range(2)]
        for dates in last_100_days:
            week_total += daily_charts_data[1][i]
            if j < 14 and dates == mondays[j]:
                print("a intrat")
                week_charts_data[0][j] = mondays[j]
                week_charts_data[1][j] = week_total
                week_total = 0
                j += 1
            i -= 1
        week_charts_data[0] = list(reversed(week_charts_data[0]))
        week_charts_data[1] = list(reversed(week_charts_data[1]))

        charts_data = [daily_charts_data, week_charts_data]

        return Response(charts_data)


def slept_hours_save(request):
    user = request.user
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SaveTime(request.POST)
        # check whether it's valid:
        if form.is_valid():
            date = form.cleaned_data["date"]
            hours = form.cleaned_data["hours"]
            try:
                check_date = HoursSleptModel.objects.get(user=user, date=date)
                check_date.hours = hours
                check_date.save()

            except:
                hours_worked = HoursSleptModel(user=user, hours=hours, date=date)
                hours_worked.save()
            return redirect("profile", chartName="hours-slept")
    return redirect("profile", chartName="hours-slept")


class JournalsChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, username, searched_date):  # Use the get method
        try:
            user = User.objects.get(username=username)
        except:
            user = request.user

        if searched_date != "null":
            date_string = searched_date
            format_string = "%Y-%m-%d"
            date_object = datetime.strptime(date_string, format_string)

            current_date = date_object.date()
        else:
            current_date = datetime.today().date()

        today = current_date
        weekday = today.weekday()
        last_monday = today - timedelta(days=weekday)

        week_days = [last_monday + timedelta(days=i) for i in range(7)]
        daily_work_data = [[0 for _ in range(7)] for _ in range(2)]
        i = 0

        for dates in week_days:
            try:
                check_date = HoursWorkedModel.objects.get(user=user, date=dates)
                daily_work_data[0][i] = dates
                daily_work_data[1][i] = check_date.hours

            except:
                daily_work_data[0][i] = dates
                daily_work_data[1][i] = 0

            i += 1
        i = 0
        daily_sleep_data = [[0 for _ in range(7)] for _ in range(2)]
        for dates in week_days:
            try:
                check_date = HoursSleptModel.objects.get(user=user, date=dates)
                daily_sleep_data[0][i] = dates
                daily_sleep_data[1][i] = check_date.hours

            except:
                daily_sleep_data[0][i] = dates
                daily_sleep_data[1][i] = 0

            i += 1

        charts_data = [daily_work_data, daily_sleep_data]

        return Response(charts_data)
