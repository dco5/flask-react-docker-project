import json
import unittest

from project.tests.utils import add_user
from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Tests for the Users Service"""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""

        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database"""

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'jaime',
                    'email': 'jaime@mail.com'
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('jaime@mail.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a username key"""

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'jaime@mail.com'
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""

        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'jaime',
                    'email': 'jaime@mail.com'
                }),
                content_type='application/json'
            )

            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'jaime',
                    'email': 'jaime@mail.com'
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correclty."""

        user = add_user('jaime','jaime@mail.com')

        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('jaime', data['data']['username'])
            self.assertIn('jaime@mail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if no id is provided."""

        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""

        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""

        add_user('jaime','jaime@mail.com')
        add_user('carlos', 'carlos@mail.com')

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)

            self.assertIn('jaime', data['data']['users'][0]['username'])
            self.assertIn('jaime@mail.com', data['data']['users'][0]['email'])

            self.assertIn('carlos', data['data']['users'][1]['username'])
            self.assertIn('carlos@mail.com', data['data']['users'][1]['email'])

            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Ensure the main route behaves correctly when no users have been added to the database."""

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No Users!</p>', response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when users have been added to the database."""
        add_user('jaime','jaime@mail.com')
        add_user('carlos', 'carlos@mail.com')

        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertIn(b'jaime', response.data)
            self.assertIn(b'carlos', response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the database via a POST request."""

        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='juan', email='juan@mail.com'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No Users!</p>', response.data)
            self.assertIn(b'juan', response.data)

    if __name__ == '__main__':
        unittest.main()
