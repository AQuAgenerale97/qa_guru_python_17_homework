import requests
from jsonschema import validate

from schemas.schema_management import get_schema

reqres_url = "https://reqres.in"
users_url = "/api/users"
api_users_url = reqres_url + users_url


def test_get_user_by_id():
    user_id = "2"
    response = requests.get(url=api_users_url + '/' + user_id,
                            verify=False)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"


def test_get_user_not_found_by_id_():
    user_id = "200"
    response = requests.get(url=api_users_url + '/' + user_id,
                            verify=False)

    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"


def test_get_user_by_id_schema_validation():
    user_id = "1"
    response = requests.get(url=api_users_url + '/' + user_id,
                            verify=False)
    body = response.json()

    validate(body, schema=get_schema('get_users'))


def test_get_users():
    response = requests.get(url=api_users_url,
                            params={"page": 2, "per_page": 4},
                            verify=False)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"


def test_get_users_schema_validation():
    response = requests.get(url=api_users_url,
                            params={"page": 20, "per_page": 4},
                            verify=False)
    body = response.json()

    validate(body, schema=get_schema('get_users_list'))


def test_post_user():
    response = requests.post(url=api_users_url,
                             data={"name": "Leo", "job": "leader"},
                             verify=False)

    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"


def test_post_user_schema_validation():
    response = requests.post(url=reqres_url + users_url,
                             data={"name": "Leo", "job": "leader"},
                             verify=False)
    body = response.json()

    validate(body, schema=get_schema('post_users'))


def test_put_user():
    user_id = '2'
    response = requests.put(url=api_users_url + '/' + user_id,
                            data={"name": "Leo", "job": "qa"},
                            verify=False)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"


def test_put_user_schema_validation():
    user_id = '1'
    response = requests.put(url=reqres_url + users_url + '/' + user_id,
                            data={"name": "Hans", "job": "leader"},
                            verify=False)
    body = response.json()

    validate(body, schema=get_schema('put_users'))


def test_schema_validate_first_name_and_email_and_job():
    first_name = 'Hans'
    email = 'leader@ld.ru'
    job = 'leader'
    user_id = '1'

    response = requests.put(url=reqres_url + users_url + '/' + user_id,
                            data={"first_name": first_name, "email": email, "job": job},
                            verify=False)
    body = response.json()

    assert response.status_code == 200
    assert body['first_name'] == first_name
    assert body['email'] == email
    assert body['job'] == job


def test_delete_user():
    user_id = '2'
    response = requests.delete(url=api_users_url + '/' + user_id,
                               verify=False)

    assert response.status_code == 204, f"Unexpected status code: {response.status_code}"


def test_job_name_from_request_returns_in_response():
    job = "master"
    name = "morpheus"

    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job})
    body = response.json()

    assert body["name"] == name
    assert body["job"] == job


def test_get_users_returns_unique_users():
    response = requests.get(
        url="https://reqres.in/api/users",
        params={"page": 2, "per_page": 4},
        verify=False
    )
    ids = [element["id"] for element in response.json()["data"]]

    assert len(ids) == len(set(ids))
