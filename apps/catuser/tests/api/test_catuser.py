import pytest

from CatFM.fixtures import api_client

from apps.catuser.models import CatUser
from apps.catuser.tests.fixtures import catuser


@pytest.mark.django_db
class TestCatUserAPI(object):
    def test_catuser_read_list_fail_no_auth(self, api_client):
        """
        Test that reading the list of users through the API fails if no authentication is provided.

        Given a GET request to the users endpoint without any authentication headers,
        the request should fail and the HTTP response code should be 401 (Unauthorized).
        """
        response = api_client.get('/users/')
        assert response.status_code == 401

    def test_catuser_read_list_fail_no_permissions(self, api_client, catuser):
        """
        Test that reading the list of users through the API fails if the user does not have permissions.

        Given a GET request to the users endpoint with an authentication token that lacks proper permissions,
        the request should fail and the HTTP response code should be 400 (Bad Request).
        """
        response = api_client.get('/users/', headers={
            'Authorization': "Token {}".format(catuser.auth_token.key)
        })
        assert response.status_code == 400

    def test_catuser_read_detail_success(self, api_client, catuser):
        """
        Test that reading the details of a specific user through the API succeeds.

        Given a GET request to the users endpoint with the ID of a specific user
        and valid authentication headers, the request should succeed and return
        the user details with an HTTP response code of 200 (OK). The response
        body contains a JSON object with the user's ID.
        """
        response = api_client.get('/users/{}/'.format(catuser.id), headers={
            'Authorization': "Token {}".format(catuser.auth_token.key)
        })
        assert response.status_code == 200
        assert response.data['id'] == catuser.id

    def test_catuser_read_detail_fail_cannot_read_other_user(self, api_client, catuser):
        """
        Test that reading the details of a specific user through the API fails if the request is made by
        another user.

        Given a GET request to the users endpoint with the ID of another user, the request should fail
        and the HTTP response code should be 400 (Bad Request).
        """
        another_user = CatUser.objects.create_user(
            email='xAn2B@example.com',
            password='password',
            first_name='John',
            last_name='Doe'
        )
        response = api_client.get('/users/{}/'.format(another_user.id), headers={
            'Authorization': "Token {}".format(catuser.auth_token.key)
        })
        assert response.status_code == 400

    def test_catuser_create_normal_user(self, api_client):
        """
        Test that creating a normal user through the API succeeds.

        Given a valid JSON payload and a POST request to the users
        endpoint, a normal user is created and the HTTP response code
        is 201 (Created).
        """
        response = api_client.post('/users/', {
            'email': 'Ih4bM@example.com',
            'password': 'password',
            'first_name': 'John',
            'last_name': 'Doe'
        }, format='json')

        assert response.status_code == 201

    def test_catuser_create_superuser_fallback(self, api_client):
        """
        Test that creating a superuser through the API does not automatically
        set the is_superuser and is_staff flags to True. The fallback behavior
        ensures that these flags remain False unless explicitly set by the system.
        """
        response = api_client.post('/users/', {
            'email': 'Ih4bM@example.com',
            'password': 'password',
            'first_name': 'John',
            'last_name': 'Doe',
            'is_superuser': True,
            'is_staff': True
        }, format='json')

        assert response.status_code == 201

        user = CatUser.objects.get(id=response.data['id'])
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_catuser_login_success(self, api_client, catuser):
        """
        Test that logging in a normal user through the API succeeds.

        Given a valid JSON payload with email and password, and a POST request
        to the users endpoint, the user is logged in and the HTTP response code
        is 200 (OK). The response body contains a JSON object with the user ID
        and an authentication token that can be used for subsequent requests.
        """
        response = api_client.post('/users/login/', {
            'email': 'Ih4bM@example.com',
            'password': 'password'
        }, format='json')

        assert response.status_code == 200
        assert response.data['token']
        assert catuser.id == response.data['id']
        assert catuser.auth_token.key == response.data['token']

    def test_catuser_login_fail_wrong_credentials(self, api_client, catuser):
        """
        Test that logging in a normal user through the API fails when the
        password is incorrect.

        Given a valid JSON payload with email and an invalid password, and a
        POST request to the users endpoint, the user is not logged in and
        the HTTP response code is 400 (Bad Request).
        """
        response = api_client.post('/users/login/', {
            'email': 'Ih4bM@example.com',
            'password': 'INVALID_PASSWORD'
        }, format='json')

        assert response.status_code == 400

    def test_catuser_login_fail_non_existing_user(self, api_client, catuser):
        """
        Test that logging in with a non-existing user through the API fails.

        Given a JSON payload with a non-existing email and any password,
        when a POST request is made to the users login endpoint,
        the login attempt should fail, and the HTTP response code should be 400 (Bad Request).
        """
        response = api_client.post('/users/login/', {
            'email': 'NON_EXISTING_USER@example.com',
            'password': 'INVALID_PASSWORD'
        }, format='json')

        assert response.status_code == 400

    def test_catuser_change_password_success(self, api_client, catuser):
        """
        Test that changing the password of a normal user through the API succeeds.

        Given a valid JSON payload with the new password and a PATCH request to the users
        endpoint, the password of the user is changed and the HTTP response code is 200 (OK).

        Furthermore, the user can be logged in with the new password and the old password is no
        longer valid.
        """
        response = api_client.patch('/users/{}/change_password/'.format(catuser.id), {
            'password': 'new_password'
        }, headers={
            'Authorization': 'Token {}'.format(catuser.auth_token.key)
        })
        assert response.status_code == 200

        catuser.refresh_from_db()
        assert catuser.check_password('new_password')

    def test_catuser_change_fail_cannot_change_password_from_other_user(self, api_client, catuser):
        """
        Test that changing the password of a normal user through the API fails when the request is made by
        another user.

        Given a valid JSON payload with the new password and a PATCH request to the users endpoint with the
        ID of another user, the password of another user is not changed and the HTTP response code is 400 (Bad Request).
        """
        another_user = CatUser.objects.create_user(
            email='xAn2B@example.com',
            password='password',
            first_name='John',
            last_name='Doe'
        )
        response = api_client.patch('/users/{}/change_password/'.format(another_user.id), {
            'password': 'new_password'
        }, headers={
            'Authorization': 'Token {}'.format(catuser.auth_token.key)
        })
        assert response.status_code == 400

    def test_catuser_delete_success(self, api_client, catuser):
        """
        Test that deleting a normal user through the API succeeds.

        Given a DELETE request to the users endpoint with the ID of a normal user,
        the user is deleted and the HTTP response code is 204 (No Content).
        """
        response = api_client.delete('/users/{}/'.format(catuser.id), headers={
            'Authorization': 'Token {}'.format(catuser.auth_token.key)
        })
        assert response.status_code == 204

    def test_catuser_delete_fail_cannot_delete_other_user(self, api_client, catuser):
        """
        Test that deleting another user through the API fails.

        Given a DELETE request to the users endpoint with the ID of another user,
        the user is not deleted and the HTTP response code is 400 (Bad Request).
        """
        another_user = CatUser.objects.create_user(
            email='xAn2B@example.com',
            password='password',
            first_name='John',
            last_name='Doe'
        )
        response = api_client.delete('/users/{}/'.format(another_user.id), headers={
            'Authorization': 'Token {}'.format(catuser.auth_token.key)
        })
        assert response.status_code == 400

    def test_catuser_update_user_success(self, api_client, catuser):
        """
        Test that updating a user through the API succeeds with partial data.

        Given a valid JSON payload with new user data and a PATCH request to the users endpoint,
        the user's first name and last name are updated and the HTTP response code is 202 (Accepted).

        The email and password fields are not updated as they are restricted.
        """
        response = api_client.patch('/users/{}/'.format(catuser.id), {
            'email': 'NEW_EMAIL@example.com',
            'first_name': 'Johnny',
            'last_name': 'Doeman',
            'password': 'new_password'
        }, headers={
            'Authorization': 'Token {}'.format(catuser.auth_token.key)
        })
        assert response.status_code == 200

        catuser.refresh_from_db()
        assert catuser.first_name == 'Johnny'
        assert catuser.last_name == 'Doeman'

        assert not catuser.check_password('new_password')
        assert not catuser.email == 'NEW_EMAIL@example.com'

    def test_catuser_update_user_fail_cannot_update_other_user(self, api_client, catuser):
        """
        Test that updating another user through the API fails.

        Given a valid JSON payload with new user data and a PATCH request to the users endpoint
        with the ID of another user, the user is not updated and the HTTP response code is 400 (Bad Request).
        """
        another_user = CatUser.objects.create_user(
            email='xAn2B@example.com',
            password='password',
            first_name='John',
            last_name='Doe'
        )
        response = api_client.patch('/users/{}/'.format(another_user.id), {
            'email': 'NEW_EMAIL@example.com',
            'first_name': 'Johnny',
            'last_name': 'Doeman',
            'password': 'new_password'
        }, headers={
            'Authorization': 'Token {}'.format(catuser.auth_token.key)
        })
        assert response.status_code == 400
