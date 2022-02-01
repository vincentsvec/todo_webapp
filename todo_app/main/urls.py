from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lists/<str:list_id>", views.lists),
    path("important/", views.important),
    path("this-week/", views.this_week),
    path("quick-tasks/", views.quick_tasks),
]
