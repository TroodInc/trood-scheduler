import factory
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django_celery_results.models import TaskResult


class PeriodFactory(factory.DjangoModelFactory):
    every = 2
    period = IntervalSchedule.MINUTES

    class Meta:
        model = IntervalSchedule


class TaskFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "task{}".format(n))
    task = "demo.test_agent"
    interval = factory.SubFactory(PeriodFactory)

    class Meta:
        model = PeriodicTask


class ResultFactory(factory.DjangoModelFactory):
    result = factory.Sequence(lambda n: "result {}".format(n))

    class Meta:
        model = TaskResult
