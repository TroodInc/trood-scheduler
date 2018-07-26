from datetime import datetime
from django.conf import settings
from scheduler.celery import app
from custodian.client import Client

from trood_auth_client.authentication import get_service_token
client = Client(settings.CUSTODIAN_URL, authorization_token=get_service_token())


@app.task
def update_task_status():
    """
    Ref T3-237
    """
    task_obj = client.objects.get('task')
    datetime_now = '{0:%Y%m%dT%H%M%S}'.format(datetime.now())
    overdued_tasks = client.records.query(task_obj).filter(status__eq='ACTIVE',
                                                           deadline__lt=datetime_now)
    for task in overdued_tasks:
        task.status = 'OVERDUE'
        task_overdue = client.records.update(task)