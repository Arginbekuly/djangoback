#Python modules
from typing import Any

#Django modules
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    DateField,
    IntegerField,
    DateTimeField,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone

#Project modules
from apps import models
from apps.abstracts.models import AbstractBaseModel
from apps.auths.validators import (
    validatate_email_domain,
    validate_email_payload_not_in_fullname,
    validate_phone,
)

class CustomUserManager(BaseUserManager):
    """
    Custom User Manager to make database requests. 
    """

    def __obtain_user_instance(
            self,
            email: str,
            full_name: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Get user instance"""
        if not email:
            raise ValidationError(
                message="Email field is required",code = "email_empty"
            )
        if not full_name:
            raise ValidationError(
                message ="Full name is required", code = "full_name_empty"
            )
        new_user: 'CustomUser' = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            password = password,
            **kwargs,
        )
        return new_user
    

    def create_user(
            self,
            email: str,
            full_name: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create Custom user. TODO where is this used?"""
        new_user : 'CustomUser' = self.__obtain_user_instance(
            email = email,
            full_name = full_name,
            password = password,
            **kwargs,
        ) 
        new_user.set_password(password)
        new_user.save(using = self.db)
        return new_user
    

    def create_superuser(
            self,
            email: str,
            full_name: str,
            password: str,
            **kwargs: dict[Any, Any]
    ) -> 'CustomUser':
        """Create Custom superuser. Used by manage.py createsuperuser"""
        new_user : 'CustomUser' = self.__obtain_user_instance(
            email = email,
            full_name = full_name,
            password = password,
            is_staff = True,
            is_superuser =True,
            **kwargs,
        ) 
        new_user.set_password(password)
        new_user.save(using = self.db)
        return new_user


class CustomUser(AbstractBaseUser,PermissionsMixin,AbstractBaseModel):
    """
    Custom user model extending AbstractBaseModel.
    """
    EMAIL_MAX_LENGTH = 150
    FULL_NAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 254
    PHONE_MAX_LENGTH = 11

    ROLES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
    )
    email = EmailField(
        max_length = EMAIL_MAX_LENGTH,
        unique = True,
        db_index = True,
        validators = [validatate_email_domain],
        verbose_name = "Email address",
        help_text = "User`s email address" ,
    )
    full_name = CharField(
        max_length = FULL_NAME_MAX_LENGTH,
        verbose_name = "Full name",
        help_text = 'User`s full name',
    )
    password = CharField(
        max_length = PASSWORD_MAX_LENGTH,
        validators = [validate_password],
        verbose_name = "Password",
        help_text = "User's hash representation of the password",
    )
    phone = CharField(
        max_length = PHONE_MAX_LENGTH,
        validators = [validate_phone],
        blank = True,
        verbose_name = "Phone number",
        help_text = "The phone number must be from 11.",
    )
    city = CharField(
        max_length = 255,
        blank = True,
        verbose_name = "City",
        help_text = "City where the user lives"
    )
    country = CharField(
        max_length = 255,
        blank = True,
        verbose_name = "Country",
        help_text = "Country where the user lives",
    )
    department = CharField(
        max_length = 255,
        blank = True,
        verbose_name = "Department",
        help_text = "User`s department (e.g., IT, HR, Sales, Finance)",
    )
    role = CharField(
        max_length = 255,
        blank = True,
        choices = ROLES,
        default = "employee",
        verbose_name = "Role",
        help_text = "User`s role in company",
    )
    birth_date = DateField(
        null = True,
        blank = True,
        verbose_name = "Birth Date",
        help_text = "User`s date of birth",
    )
    salary = IntegerField(
        null = True,
        blank = True,
        verbose_name = "Salary",
        help_text = "User`s salary per month",
    )
    is_active = BooleanField(
        default = True,
        verbose_name = "Active",
        help_text = "Whether this user account is active",
    )
    is_staff = BooleanField(
        default = False,
        verbose_name = "Staff Status",
        help_text = "Defines if user can access the admin panel",
    )
    data_joined = DateTimeField(
        default = timezone.now,
        verbose_name = "Data Joined",
        help_text = "The date when the user registered",
    )
    last_login = DateTimeField(
        null = True,
        blank = True,
        verbose_name = "Last login",
        help_text = "Last login timestamp",
    )
    REQUIRED_FIELDS = ["full_name"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        """Meta option for CustomerUser model"""

        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ["-created_at"]

    def clean(self) -> None:
        """Validate the model instance before saving."""
        validate_email_payload_not_in_fullname(
            email=self.email,
            full_name=self.full_name,
        )
        return super().clean()
