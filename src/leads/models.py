from django.db import models

from account.models import Account
from core.fields import UUIDPrimaryKey


def profile_picture_path(instance, filename):
    return f'qr-codes/{instance.pk}.png'


class Lead(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        limit_choices_to={'registration__isnull': False},
    )
    group = models.ForeignKey(
        "LeadGroup",
        on_delete=models.PROTECT,
        related_name="+",
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.user.username


class LeadCode(models.Model):
    id = UUIDPrimaryKey()
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    code_image = models.ImageField(upload_to=profile_picture_path)

    def __str__(self):
        return str(self.account)


class LeadGroup(models.Model):
    name = models.CharField(max_length=120, unique=True)
    admins = models.ManyToManyField(
        Account,
        related_name='+',
        limit_choices_to={'registration__isnull': False},
    )
    leads = models.ManyToManyField(
        Account,
        blank=True,
        through=Lead,
        related_name='+',
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_for_user(cls, user):
        return cls.objects.filter(admins=user.account).last()
