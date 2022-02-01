from .forms import NewList, NewTask
from .models import Lists, Task
from .custom_context import order_lists


class Requests:
    def __init__(self, response, listview):
        self.response = response
        self.listview = listview

    def check(self):
        task = self.listview.get(id=self.response.POST.get("check"))
        task.complete = True
        task.save()

    def uncheck(self):
        task = self.listview.get(id=self.response.POST.get("uncheck"))
        task.complete = False
        task.save()

    def update_list(self):
        task_id = self.response.POST.get("list-id")
        self.listview = self.response.user.lists.get(id=task_id)

        if self.response.POST.get("update-list") != "delete-#hw30fwn3":
            self.listview.name = self.response.POST.get("update-list")
            self.listview.save()

        else:
            task_id = self.response.POST.get("list-id")
            self.listview.delete()

    def delete_task(self):
        self.listview.get(id=self.response.POST.get("delete-task")).delete()

    def add_important(self):
        task = self.listview.get(id=self.response.POST.get("add-important"))
        task.important = True
        task.save()

    def remove_important(self):
        task = self.listview.get(
            id=self.response.POST.get("remove-important"))
        task.important = False
        task.save()

    def task_edit(self):
        task = self.listview.get(id=self.response.POST.get("task-id"))
        task.name = self.response.POST.get("task-edit")
        task.subnote = self.response.POST.get("task-edit-sn")

        if self.response.POST.get("task-edit-dt") != "":
            task.due_date = self.response.POST.get("task-edit-dt")

        task.save()


def check_post(response, listview):
    '''
    checks for post requests
    '''

    requests = Requests(response, listview)

    requests_list = {
        'check': requests.check,
        'uncheck': requests.uncheck,
        'update-list': requests.update_list,
        'delete-task': requests.delete_task,
        'add-important': requests.add_important,
        'remove-important': requests.remove_important,
        'task-edit': requests.task_edit,
    }

    for request in requests_list:
        if request in response.POST:
            requests_list[request]()
            break


def check_post_tl(response, listview=None):
    '''
    checks post requsts of list and task add on all views
    '''

    form = NewList(response.POST)
    form_task = NewTask(response.POST)

    if response.method == "POST" and 'addtask' not in response.POST:

        if form.is_valid():
            name = form.cleaned_data["name"]

            tdlist = Lists(name=name)
            tdlist.save()
            response.user.lists.add(tdlist)

    elif response.method == "POST" and 'addtask' in response.POST:

        if form_task.is_valid():

            name = form_task.cleaned_data["name"]

            if response.POST.get('due_date') != "":
                due_date = response.POST.get('due_date')
            else:
                due_date = None

            notes = response.POST.get('subnotes')

            lists_id = listview.id
            task = Task(name=name, complete=False,
                        due_date=due_date, lists_id=lists_id, user_id=response.user.id, subnote=notes)
            task.save()

    # prevents from autocompleting values into input fields
    form_task = NewTask(None)
    form = NewList(None)

    return form_task, form
