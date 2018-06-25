from rest_framework import viewsets
from django_celery_beat.models import PeriodicTask
from django_celery_results.models import TaskResult
from rest_framework.permissions import IsAuthenticated

from scheduler.api.serializers import TaskSerializer, ResultSerializer


class TasksViewset(viewsets.ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)


class ResultsViewset(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = ResultSerializer
    permission_classes = (IsAuthenticated,)
