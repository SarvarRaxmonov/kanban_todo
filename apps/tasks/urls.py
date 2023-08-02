from django.urls import path
from rest_framework import routers

from apps.tasks.views import BoardView, ColumnView, LoginView, RegisterView, SubTaskView, TaskView

router = routers.DefaultRouter()

urlpatterns = [
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("task/update/<int:pk>", TaskView.as_view(), name="task-update"),
    path("task/", TaskView.as_view(), name="task"),
    path("sub-task/", SubTaskView.as_view({"get": "list"}), name="sub-task"),
    path(
        "sub-task/update/<int:pk>",
        SubTaskView.as_view({"get": "get_object"}),
        name="sub-task-update",
    ),
    path(
        "sub-task/delete/<int:pk>",
        SubTaskView.as_view({"delete": "destroy"}),
        name="sub-task-delete",
    ),
    path("column/", ColumnView.as_view({"get": "list"}), name="column"),
    path(
        "column/update/<int:pk>",
        ColumnView.as_view({"get": "put"}),
        name="column-update",
    ),
    path("board/", BoardView.as_view({"get": "list"}), name="board"),
]
