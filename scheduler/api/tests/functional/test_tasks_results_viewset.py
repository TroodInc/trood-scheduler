import pytest
from django.test import Client
from rest_framework import status
from rest_framework.reverse import reverse
from hamcrest import *

from scheduler.api.tests.factories import ResultFactory


@pytest.mark.django_db
def test_can_retrieve_task_results(client: Client):
    result = ResultFactory()

    response = client.get(reverse('api:results-list'))
    decoded_response = response.json()

    assert_that(response.status_code, equal_to(status.HTTP_200_OK))
    assert_that(len(decoded_response), equal_to(1))
    assert_that(decoded_response[0]['result'], equal_to(result.result))
