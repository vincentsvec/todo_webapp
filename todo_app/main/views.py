from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Lists, Task
from .forms import NewTask, NewList
from .requests import check_post_tl, check_post
from .custom_context import order_lists
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import Case, When
import json


@login_required
def index(response):
    '''
    1. Today page of the app. Filters tasks by date and displays them on page.
    If user is not authenticated redirectsto login.
    2. Builds form for adding new list
    '''

    tasks = response.user.tasks.all()
    date = datetime.today().strftime('%Y-%m-%d')

    def today_tasks():
        for task in tasks:
            if str(task.due_date) == date:
                yield task

    # gets order of lists passed by javascript into post request after sorting ends
    order_lists(response)

    form_task, form = check_post_tl(response)

    if response.method == "POST":
        check_post(response, tasks)
        return redirect("/")

    return render(response, "main/today.html",
                  {"tasks": today_tasks(), "form": form, "form_task": form_task})


@login_required
def lists(response, list_id):
    '''
    1. finds list view, if exists redirects if not redirects to 404
    and posts new task in list view
    2. saves task checkbox values
    3. checks for list delete and deletes it
    4. checks for task delete and deletes it
    5. add or removes important tasks
    '''

    # gets order of lists passed by javascript into post request after sorting ends
    order_lists(response)

    '''listview = get_object_or_404(
        response.user.lists, id=int(list_id))'''

    listview = response.user.lists.filter(id=int(list_id)).first()

    # redirects home if list does not exist
    if listview == None:
        return redirect('/')

    # order by id
    tasks = listview.task_set.all().order_by("id")

    form_task, form = check_post_tl(response, listview)

    if response.method == "POST":
        check_post(response, listview.task_set)

        return redirect("/lists/" + str(listview.id))

    return render(response, "main/list.html", {"tasks": tasks, "form_task": form_task, "form": form, "listname": listview.name, "listid": listview.id})


@login_required
def important(response):
    '''
    Lists all important tasks
    '''

    # gets order of lists passed by javascript into post request after sorting ends
    order_lists(response)

    tasks = response.user.tasks.filter(important=True).order_by("id")

    if response.method == "POST":
        check_post(response, tasks)

    form_task, form = check_post_tl(response)

    return render(response, "main/important.html", {"form": form, "form_task": form_task, "tasks": tasks})


@login_required
def this_week(response):
    '''
    Displays all tasks this week
    '''

    tasks = response.user.tasks.all()
    form_task, form = check_post_tl(response)

    def week_tasks():
        for task in tasks:
            if task.due_date != None:
                date = task.due_date
                tday = datetime.today()

                if date.strftime("%V") == tday.strftime("%V"):
                    yield task

    # gets order of lists passed by javascript into post request after sorting ends
    order_lists(response)

    if response.method == "POST":
        check_post(response, tasks)
        return redirect("/this-week")

    return render(response, "main/thisweek.html", {"form": form, "form_task": form_task, "tasks": week_tasks()})


@login_required
def quick_tasks(response):
    '''
    View for adding quick tasks. List has value of default = True. 
    '''

    # gets order of lists passed by javascript into post request after sorting ends
    order_lists(response)

    tasks = response.user.tasks.all()

    # adds quick-tasks list if user is new
    if response.user.lists.filter(name="quick-tasks").first() == None:
        tdlist = Lists(name="quick-tasks", default=True, order=-1)
        tdlist.save()
        response.user.lists.add(tdlist)

    if response.method == "POST":
        check_post(response, tasks)

    listview = response.user.lists.get(default=True)
    tasks = listview.task_set.all().order_by("id")

    form_task, form = check_post_tl(response, listview)

    return render(response, "main/quicktasks.html", {"form": form, "form_task": form_task, "tasks": tasks})
