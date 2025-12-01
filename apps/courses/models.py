#Django modules
from django.db.models import (
    CharField,
    BooleanField,
    TextField,
    ForeignKey,
    DecimalField,
    CASCADE,
    PositiveSmallIntegerField,
)
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator

#Project modules
from apps.abstracts.models import AbstractBaseModel

class Courses(AbstractBaseModel):
    """Courses model."""
    MAX_TITLE_LENGTH = 128

    title = CharField(max_length=128)
    description = TextField(
        blank = True,
        null = True,
        verbose_name = "Description",
    )
    is_active = BooleanField(
        default = True,
        verbose_name = "Is active",
    )
    owner = ForeignKey(
        to = get_user_model(),
        related_name = "owned_courses",
        verbose_name = "Owner",
        on_delete = CASCADE,
    )
    
    class Meta:
        """class Meta."""
        default_related_name = "owned_courses"


class Lesson(AbstractBaseModel):
    """Lesson model"""
    MAX_TITLE_LENGTH = 128

    course = ForeignKey(
        to = Courses,
        related_name = "lessons",
        verbose_name = "Lessons",
        on_delete = CASCADE,
    )
    title = CharField(max_length=MAX_TITLE_LENGTH, verbose_name = "Title",)
    content = TextField(
        blank = True,
        null = True,
        verbose_name = "Content",
    )
    order = DecimalField(
        max_digits = 5,
        decimal_places = 2,
        default = 1.0,
        null = True,
        verbose_name = "Order",
    )
    indentation = PositiveSmallIntegerField(
        validators = [MaxValueValidator(5)],
        verbose_name = "Identation",
    )
    is_published = BooleanField(
        default = False,
        verbose_name = "Is published"
    )
