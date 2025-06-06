from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password

from model_utils.managers import InheritanceManager

from apps.core.models import BaseModel


class UserManagerCustom(UserManager, InheritanceManager):

    def get_queryset(self):
        return super(InheritanceManager, self).get_queryset().select_subclasses()

    def _get_model_to_create(self, role):
        if role == 'client':
            return ClientUser
        elif role == 'freelancer':
            return FreelancerUser
        elif role == 'superuser':
            return SuperUser
        raise ValueError('There is no role with this name %s' % role)

    def _create_user(self, username, email, password, role, **extra_fields):
        """
            Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        username = BaseModel.normalize_username(username)
        model = self._get_model_to_create(role=role)
        user = model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, role=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, role, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, 'superuser', **extra_fields)


class BaseUser(BaseModel, AbstractUser):
    USER_ROLE_AVAILABLE = [
        'client', 'freelancer'
    ]

    ALL_USER_ROLE_AVAILABLE = [
        *USER_ROLE_AVAILABLE,
        'superuser'
    ]

    role = None

    objects = UserManagerCustom()

    class Meta:
        ordering = '-created_at',


class ClientUser(BaseUser):
    role = models.CharField(max_length=10, default='client', editable=False)


class FreelancerUser(BaseUser):
    role = models.CharField(max_length=12, default='freelancer', editable=False)


class SuperUser(BaseUser):
    role = models.CharField(max_length=10, default='superuser', editable=False)
