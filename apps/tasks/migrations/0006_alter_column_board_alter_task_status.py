# Generated by Django 4.2.1 on 2023-08-02 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0005_alter_task_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="column",
            name="board",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chosen_board",
                to="tasks.board",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="chosen_tasks",
                to="tasks.column",
            ),
        ),
    ]
