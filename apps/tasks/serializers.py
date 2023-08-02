from django.contrib.auth.models import User
from rest_framework import serializers

from apps.tasks.models import Board, Column, SubTask, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ("title", "is_done")


class TaskSerializer(serializers.ModelSerializer):
    board_name = serializers.ReadOnlyField(source="status.board.name")

    class Meta:
        model = Task
        fields = (
            "title",
            "user",
            "description",
            "sub_tasks",
            "status",
            "board_name",
        )


class ColumnSerializer(serializers.ModelSerializer):
    chosen_tasks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Column
        fields = ("name", "board", "chosen_tasks")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get("user_id")
        if user is not None:
            self.fields["board"].queryset = Board.objects.filter(user=user)


class BoardSerializer(serializers.ModelSerializer):
    chosen_column = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ("name", "chosen_column")
