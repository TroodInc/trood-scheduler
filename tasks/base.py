import requests
from requests import RequestException
from celery.task import task

from trood.core.utils import get_service_token


@task()
def simple_http_call(url, method="get", use_auth=True, **kwargs):
    try:
        headers = {}
        if use_auth:
            headers = {"Authorization": get_service_token()}

        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()

        result = {
            'status': response.status_code,
            'responce': response.json()
        }

    except RequestException as e:
        result = {
            'status': 'Failed with exception',
            # 'response': e.response,
            # 'request': e.request
        }

    return result
