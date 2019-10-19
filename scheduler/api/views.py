from rest_framework import viewsets
from django_celery_beat.models import PeriodicTask
from django_celery_results.models import TaskResult

from scheduler.api.serializers import TaskSerializer, ResultSerializer


class TasksViewset(viewsets.ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = TaskSerializer


class ResultsViewset(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = ResultSerializer
