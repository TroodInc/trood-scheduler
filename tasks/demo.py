import datetime
from celery import shared_task, task


@task()
def test_agent():
    return "Test agent was called at {}".format(datetime.datetime.now())
