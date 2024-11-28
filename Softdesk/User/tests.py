from django.test import TestCase
from datetime import date

from .models import User


class UserModelTestCase(TestCase):

    def test_is_of_age_exactly_15(self):
        # Utilisateur ayant exactement 15 ans aujourd'hui
        today = date.today()
        birth_date = date(today.year - 15, today.month, today.day)
        user = User(date_of_birth=birth_date)
        self.assertTrue(user.is_of_age(15))

    def test_is_of_age_just_under_15(self):
        # Utilisateur ayant 14 ans et 364 jours
        today = date.today()
        birth_date = date(today.year - 15, today.month, today.day + 1)
        user = User(date_of_birth=birth_date)
        self.assertFalse(user.is_of_age(15))

    def test_is_of_age_over_15(self):
        # Utilisateur ayant plus de 15 ans
        today = date.today()
        birth_date = date(today.year - 16, today.month, today.day)
        user = User(date_of_birth=birth_date)
        self.assertTrue(user.is_of_age(15))

    def test_is_of_age_far_under_15(self):
        # Utilisateur ayant beaucoup moins de 15 ans
        today = date.today()
        birth_date = date(today.year - 10, today.month, today.day)
        user = User(date_of_birth=birth_date)
        self.assertFalse(user.is_of_age(15))
