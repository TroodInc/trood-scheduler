from rest_framework import serializers

from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django_celery_results.models import TaskResult
from rest_framework.exceptions import ValidationError


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class TaskSerializer(serializers.ModelSerializer):
    schedule = serializers.CharField()

    class Meta:
        model = PeriodicTask
        fields = (
            'name', 'task', 'args', 'kwargs', 'enabled', 'last_run_at',
            'total_run_count', 'description', 'schedule'
        )
        write_only_fields = ('schedule', )

    def create(self, validated_data):
        schedule = validated_data.pop('schedule', None)

        if is_number(schedule):
            interval, _ = IntervalSchedule.objects.get_or_create(every=int(schedule), period=IntervalSchedule.SECONDS)
            validated_data['interval'] = interval

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
                validated_data['crontab'] = crontab
            else:
                raise ValidationError("Wrong crontab string: {}".format(schedule))

        else:
            raise ValidationError("Wrong schedule string: {}".format(schedule))

        return super(TaskSerializer, self).create(validated_data)


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ('task_id', 'status', 'result', 'date_done', 'traceback', )
