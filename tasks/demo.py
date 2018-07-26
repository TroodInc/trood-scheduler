import datetime
from celery import shared_task, task
from scheduler.celery import app


@task()
def test_agent():
    return "Test agent was called at {}".format(datetime.datetime.now())


@app.task
def test_print_ok():
    print('PRINTING OK')
    return "Printing was called at {}".format(datetime.datetime.now())
