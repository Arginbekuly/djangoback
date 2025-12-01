#Python modules
from typing import Any

#Django modules
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


