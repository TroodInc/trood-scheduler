import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from hamcrest import *
from rest_framework.test import APITestCase, APIClient

from scheduler.api.tests.factories import ResultFactory
from trood_auth_client.authentication import TroodUser

trood_user = TroodUser({
    "id": 1,
})


class TaskResultTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=trood_user)

    @pytest.mark.django_db
    def test_can_retrieve_task_results(self):
        result = ResultFactory()

        response = self.client.get(reverse('api:results-list'))
        decoded_response = response.json()

        assert_that(response.status_code, equal_to(status.HTTP_200_OK))
        assert_that(len(decoded_response), equal_to(1))
        assert_that(decoded_response[0]['result'], equal_to(result.result))
