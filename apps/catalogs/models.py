#Django modules
from django.db.models import (
    Model, 
    CharField, 
    TextField, 
    FloatField,
    BooleanField, 
    ForeignKey,
    ManyToManyField,
    CASCADE, 
)

from django.core.validators import MinValueValidator


class Restaurant(Model):
    """
    Model of the restarant
    """

    MAX_NAME_LENGTH = 100

    name = CharField(max_length=MAX_NAME_LENGTH)
    description = TextField()

class MenuItem(Model):
    """
    Model representing item in restaurant
    """

    MAX_NAME_LENGTH = 100

    restaurant_id = ForeignKey(to=Restaurant, on_delete=CASCADE, related_name="menu_items")

    name = CharField(max_length=MAX_NAME_LENGTH)
    price = FloatField(validators=[MinValueValidator(0,0)])
    availability = BooleanField(default=True)

class Category(Model):
    """
    Model of the categories
    """

    MAX_NAME_LENGTH = 100
    name = CharField(max_length=MAX_NAME_LENGTH)

class MenuItemCategory(Model):
    """
    Model representing many-to-many between MenuItem and Category
    """

    menu_item_id = ManyToManyField(to=MenuItem, related_name="categories")
    category_id = ManyToManyField(to=Category, related_name="menu_items")

class Option(Model):
    """
    Model representing options of the. menu item
    """

    MAX_NAME_LENGTH = 100

    menu_item_id = ForeignKey(to=MenuItem, on_delete=CASCADE, related_name="options")

    name = CharField(max_length=MAX_NAME_LENGTH)


class ItemOption(Model):
    """
    Model representing the many-to-many between MenuItem and Option
    """

    menu_item_id = ManyToManyField(to=MenuItem, related_name="item_options")
    option_id = ManyToManyField(to=Option, blank=True, related_name="item_options")
    price_delta = FloatField(default=0.0, validators=[MinValueValidator(0,0)])
    is_default = BooleanField(default=False)