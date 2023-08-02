from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.base import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Board, Column, SubTask, Task
from apps.tasks.serializers import BoardSerializer, ColumnSerializer, SubTaskSerializer, TaskSerializer, UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            user_of_task = User.objects.get(username=request.user)
            instance = Task.objects.get(user=user_of_task.id, id=pk)
            serializer = TaskSerializer(instance)
            return Response(serializer.data)
        return Response({"Write your task": "Exapmle 1"})

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def patch(self, request, *args, **kwargs):
        instance = Task.objects.get(id=request.data.get("id"))
        serializer = TaskSerializer(data=request.data, instance=instance, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)

    def delete(self, request, pk=None, format=None):
        try:
            obj = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({"message": "Object deleted"}, status=status.HTTP_204_NO_CONTENT)


class SubTaskView(ModelViewSet):
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk=None):
        instance = SubTask.objects.get(pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def patch(self, request, *args, **kwargs):
        instance = self.get_queryset(id=request.data.get("id"))
        serializer = self.get_serializer(data=request.data, instance=instance, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_queryset().get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ColumnView(ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        instance = Column.objects.all()
        serializer = ColumnSerializer(instance, many=True, context={"user_id": request.user.id})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ColumnSerializer(data=request.data, context={"user_id": request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        instance = self.get_queryset().get(pk=pk)
        serializer = ColumnSerializer(data=request.data, instance=instance, context={"user_id": request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)

    def delete(self, request, pk=None, *args, **kwargs):
        instance = self.get_queryset().get(pk=pk, user=request.user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        context = super(ColumnView, self).get_serializer_context()
        context.update({"user_id": self.request.user.id})
        return context


class BoardView(ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, pk=None, *args, **kwargs):
        user_of_board = User.objects.get(username=self.request.user.username)
        instance = self.get_queryset().filter(user=user_of_board)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Board.objects.all()
