from rest_framework.serializers import ModelSerializer

from django_celery_beat.models import PeriodicTask
from django_celery_results.models import TaskResult


class TaskSerializer(ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = ('name', 'task', 'args', 'kwargs', 'enabled', 'last_run_at', 'total_run_count', 'description', )


class ResultSerializer(ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ('task_id', 'status', 'result', 'date_done', 'traceback', )
