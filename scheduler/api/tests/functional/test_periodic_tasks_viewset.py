import pytest
from django.test import Client
from hamcrest import *
from hamcrest.core import assert_that
from rest_framework import status
from rest_framework.reverse import reverse

from scheduler.api.tests.factories import TaskFactory


@pytest.mark.django_db
def test_can_retrieve_periodic_tasks_list(client: Client):
    task = TaskFactory()
    response = client.get(reverse('api:tasks-list'))
    decoded_response = response.json()

    assert_that(response.status_code, equal_to(status.HTTP_200_OK))
    assert_that(len(decoded_response), equal_to(1))
    assert_that(decoded_response[0]['name'], equal_to(task.name))


@pytest.mark.django_db
def test_can_create_cronlike_task(client: Client):
    task_data = {
        'name': 'test task',
        'task': 'demo.test_agent',
        'schedule': '*/10 * * * *'
    }

    response = client.post(reverse('api:tasks-list'), data=task_data)

    assert_that(response.status_code, equal_to(status.HTTP_201_CREATED))


@pytest.mark.django_db
def test_can_create_timeperiod_task(client: Client):
    task_data = {
        'name': 'test task',
        'task': 'demo.test_agent',
        'schedule': 10
    }

    response = client.post(reverse('api:tasks-list'), data=task_data)

    assert_that(response.status_code, equal_to(status.HTTP_201_CREATED))
