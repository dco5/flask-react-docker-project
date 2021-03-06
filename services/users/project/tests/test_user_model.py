import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase

from sqlalchemy.exc import IntegrityError

from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('justatest', 'mail@test.com')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'mail@test.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        user = add_user('justatest', 'mail@test.com')
        db.session.add(user)
        db.session.commit()

        duplicate_user = User(username='justatest', email='mail@test2.com')
        db.session.add(duplicate_user)

        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = add_user('justatest', 'mail@test.com')
        db.session.add(user)
        db.session.commit()

        duplicate_user = User(username='justatest2', email='mail@test.com')
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = User(username='justatest', email='mail@test.com')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(isinstance(user.to_json(), dict))


if __name__ == '__main__':
    unittest.main()
