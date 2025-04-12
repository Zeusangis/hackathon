from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
import shortuuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(_("User must have an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        _("ID"), primary_key=True, max_length=22, default=shortuuid.uuid, editable=False
    )
    email = models.EmailField(_("Email Address"), unique=True)
    full_name = models.CharField(_("Full Name"), max_length=100)
    phone = models.CharField(_("Phone Number"), max_length=15, null=True, blank=True)
    profile_image = models.ImageField(
        _("Profile Image"),
        upload_to="profile/",
        default="profile/default.png",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    is_agent = models.BooleanField(_("Is Agent"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]


class BodyMassIndex(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    height = models.FloatField(_("Height (cm)"))
    weight = models.FloatField(_("Weight (kg)"))
    bmi = models.FloatField(_("BMI"), blank=True, null=True)
    date = models.DateTimeField(_("Date"), auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.height and self.weight:
            height_m = self.height / 100
            self.bmi = self.weight / (height_m**2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.full_name} - {self.bmi}"

    class Meta:
        verbose_name = _("Body Mass Index")
        verbose_name_plural = _("Body Mass Indexes")
        ordering = ["-date"]
