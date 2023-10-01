from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


from .constants import DOCUMENT_TYPE_LIST

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(verbose_name=_("phone_number"), max_length=30)
    doc_type = models.CharField(
        verbose_name=_("document_type"),
        choices=DOCUMENT_TYPE_LIST,
        max_length=20,
        default="none",
    )
    doc_number = models.CharField(
        verbose_name=_("document_number"), max_length=30, default="none"
    )
    country = CountryField(verbose_name=_("country"), null=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
