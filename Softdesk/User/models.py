from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import date


class User(AbstractUser):
    date_of_birth = models.DateField(null=False, blank=False)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

    def calculate_age(self):
        # Calcule l'âge de l'utilisateur
        if not self.date_of_birth:
            raise ValueError("Date de naissance requise")
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month,
                                        self.date_of_birth.day)
        )

    def is_of_age(self, min_age=15):
        return self.calculate_age() >= min_age
