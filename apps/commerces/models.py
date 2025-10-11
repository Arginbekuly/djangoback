#Django modules
from django.db.models import (
    Model, 
    CharField, 
    IntegerField,
    FloatField,
    BooleanField, 
    ForeignKey,
    ManyToManyField,
    DateTimeField,
    CASCADE, 
    PROTECT
)

from django.core.validators import MinValueValidator, MaxValueValidator

#Project modules
from apps.catalogs.models import MenuItem, Option

class User(Model):
    """
    Model representing of the User
    """
    MAX_LENGTH_NAME = 100
    username = CharField(max_length=MAX_LENGTH_NAME)


class Address(Model):
    """
    Model of the address
    """

    user_id = ForeignKey(to=User, on_delete=CASCADE, related_name="addresses")



class Order(Model):
    """
    Model representing an order.
    """

    STATUS_CHOICES = (
        (0, "New"),
        (1, "Confirmed"),
        (2, "Delivering"),
        (3, "Done"),
    )

    user_id = ForeignKey(to=User,on_delete=PROTECT,related_name="orders")
    address_id = ForeignKey(to=Address, on_delete=PROTECT, related_name="orders")
    status = IntegerField(default=0,)
    total_price = FloatField(validators=[MinValueValidator(0.0)])
    subTotal_price = FloatField(validators=[MinValueValidator(0.0)])
    discount_total = FloatField(
        default=0.0, 
        validators=[
            MinValueValidator(0.0), 
            MaxValueValidator(100.0)
        ],
    )
    created_at = DateTimeField(auto_now_add=True,)
    updated_at = DateTimeField(auto_now=True,)

class OrderItem(Model):
    """
    Model representing an item in an order.
    """    

    order_id = ForeignKey(
        to=MenuItem, on_delete=CASCADE, related_name="order_items",
    )
    menu_item_name = CharField(max_length=100)
    menu_item_price = FloatField(validators=[MinValueValidator(0.0)],
    )
    quantity = IntegerField(validators=[MinValueValidator(1)])
    line_total = FloatField(validators=[MinValueValidator(0.0)])



class OrderItemOption(Model):
    """
    Model representing many-to-many between OrderItem and Option
    """

    order_item_id = ForeignKey(to=OrderItem, on_delete=CASCADE, related_name="item_options")
    option_id = ForeignKey(to=Option, on_delete=PROTECT, related_name="order_item_options")


class Promo(Model):
    """
    Model representing a promotional code.
    """

    name = CharField(max_length=20,)
    description = CharField(max_length=100,)
    discount = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = BooleanField(default=True,)


class OrderPromo(Model):
    """
    Model representing many-to-many between OrderItem and Option
    """

    order_id = ManyToManyField(to=Order, related_name="order_promos")
    promo_id = ManyToManyField(to=Promo, related_name="order_promos")