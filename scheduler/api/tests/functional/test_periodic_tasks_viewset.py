import pytest
from django.test import Client

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from scheduler.api.tests.factories import TaskFactory
from trood.contrib.django.auth.authentication import TroodUser
from scheduler.celery import app

trood_user = TroodUser({
    "id": 1,
})


class PeriodicTasksTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=trood_user)
        app.conf.update(CELERY_ALWAYS_EAGER=True)

    @pytest.mark.django_db
    def test_can_retrieve_periodic_tasks_list(self):
        task = TaskFactory()
        response = self.client.get(reverse('api:tasks-list'))
        decoded_response = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(decoded_response) == 1
        assert decoded_response[0]['name'] == task.name


    @pytest.mark.django_db
    def test_can_create_cronlike_task(self):
        task_data = {
            'name': 'test task',
            'task': 'demo.test_agent',
            'schedule': '*/10 * * * *'
        }

        response = self.client.post(reverse('api:tasks-list'), data=task_data)

        assert response.status_code == status.HTTP_201_CREATED


    @pytest.mark.django_db
    def test_can_create_timeperiod_task(self):
        task_data = {
            'name': 'test task',
            'task': 'demo.test_agent',
            'schedule': 10
        }

        response = self.client.post(reverse('api:tasks-list'), data=task_data)

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_can_create_imidiate_task(self):
        task_data = {
            'name': 'test task',
            'task': 'demo.test_print_ok',
            'schedule': 'now'
        }

        response = self.client.post(reverse('api:tasks-list'), data=task_data)

        assert response.status_code == status.HTTP_201_CREATED
