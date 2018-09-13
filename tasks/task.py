from datetime import datetime, timedelta

import requests
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


@app.task
def deadline_notification():
    #
    #          3h               2h59m           0h
    #  time____L________________'_______________| <- DEADLINE
    #          {  gap to notify }
    #
    gap = datetime.now() + timedelta(hours=3)
    start = '{0:%Y%m%dT%H%M%S}'.format(gap)
    end = '{0:%Y%m%dT%H%M%S}'.format(gap + timedelta(minutes=1, seconds=1))
    task_obj = client.objects.get('task')
    notify_tasks = client.records.query(task_obj, depth=2).filter(
        status__eq='ACTIVE', deadline__gt=start, deadline__lt=end
    )

    for task in notify_tasks:
        requests.post(
            "{}/api/v1.0/mails/from_template/".format(settings.MAIL_SERVICE_URL),
            json={
                "mailbox": settings.SYSTEM_MAIL_ID,
                "to": [task.executor['email']],
                "template": "TASK_EXPIRING",
                "data": {
                    "task_id": task.id,
                    "task_name": task.name
                }
            },
            headers={'Authorization': get_service_token()}
        )

    return list(notify_tasks)