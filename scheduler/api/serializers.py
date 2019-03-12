import json
from rest_framework import serializers

from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django_celery_results.models import TaskResult
from rest_framework.exceptions import ValidationError
import importlib


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def set_task_schedule(data):
    schedule = data.pop('schedule')
    if is_number(schedule):
        interval, _ = IntervalSchedule.objects.get_or_create(every=int(schedule), period=IntervalSchedule.SECONDS)
        data['interval'] = interval

    elif 'now' in schedule:
        task_path = data['task']
        task_module, this_task_name = task_path.split('.')
        task_module = importlib.import_module(f'tasks.{task_module}')
        task = getattr(task_module, this_task_name)

        if 'args' in data:
            args = json.loads(data['args'])
        else:
            args = list()
        
        if 'kwargs' in data:
            kwargs = json.loads(data['kwargs'])
        else:
            kwargs = dict()
        
        task.delay(*args, **kwargs)

    elif isinstance(schedule, str):
        parts = schedule.split(" ")
        if len(parts) == 5:
            crontab, _ = CrontabSchedule.objects.get_or_create(
                minute=parts[0],
                hour=parts[1],
                day_of_week=parts[2],
                day_of_month=parts[3],
                month_of_year=parts[4]
            )
            data['crontab'] = crontab
        else:
            raise ValidationError("Wrong crontab string: {}".format(schedule))

    else:
        raise ValidationError("Wrong schedule string: {}".format(schedule))
    return data



class TaskSerializer(serializers.ModelSerializer):
    schedule = serializers.CharField()
    args = serializers.ListField(required=False)
    kwargs = serializers.DictField(required=False)

    class Meta:
        model = PeriodicTask
        fields = (
            'id', 'name', 'task', 'args', 'kwargs', 'enabled', 'last_run_at',
            'total_run_count', 'description', 'schedule'
        )

    def to_internal_value(self, data):
        data = super(TaskSerializer, self).to_internal_value(data)

        if 'args' in data:
            data['args'] = json.dumps(data.get('args'))

        if 'kwargs' in data:
            data['kwargs'] = json.dumps(data.get('kwargs'))

        if 'schedule' in data:
            data = set_task_schedule(data)

        return data

    def to_representation(self, instance):
        instance.args = json.loads(instance.args)
        instance.kwargs = json.loads(instance.kwargs)

        return super(TaskSerializer, self).to_representation(instance)


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ('id', 'task_id', 'status', 'result', 'date_done', 'traceback', 'meta')
