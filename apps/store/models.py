from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CharField, ImageField, ForeignKey, CASCADE, BooleanField, TextField, ManyToManyField, \
    DecimalField, DateField, PositiveIntegerField

from apps.shared.models import AbstractBaseModel
from apps.users.models import User


class Category(AbstractBaseModel):
    name = CharField(max_length=250)
    cover = ImageField(upload_to='categories/')


class SubCategory(AbstractBaseModel):
    name = CharField(max_length=250)
    category = ForeignKey('Category', on_delete=CASCADE, related_name='sub_categories')
    cover = ImageField(upload_to='sub_categories/')


class Brand(AbstractBaseModel):
    name = CharField(max_length=250)
    cover = ImageField(upload_to='brands/')


class Discount(AbstractBaseModel):
    name = CharField(max_length=250, unique=True)
    cover = ImageField(upload_to='discounts/')
    is_active = BooleanField(default=True)


class Product(AbstractBaseModel):
    COLOR_CHOICES = [
        ('#FF5733', 'Red'),
        ('#33FF57', 'Green'),
        ('#3357FF', 'Blue'),
        ('#F3FF33', 'Yellow'),
        ('#000000', 'Black'),
        ('#FFFFFF', 'White'),
    ]

    name = CharField(max_length=250)
    description = TextField(default=f'{name} description')
    color = CharField(max_length=7, choices=COLOR_CHOICES, null=True)
    category = ForeignKey('Category', on_delete=CASCADE, related_name='products')
    sub_category = ManyToManyField('SubCategory', related_name='products')
    brand = ForeignKey('Brand', on_delete=CASCADE, related_name='products')
    discount = ManyToManyField('Discount', related_name='products')
    price = DecimalField(max_digits=10, decimal_places=2)
    published_at = DateField(null=True)
    is_active = BooleanField(default=True)
    like_count = PositiveIntegerField(default=0)
    review_count = PositiveIntegerField(default=0)

    def __str__(self):
        return self.get_color_display()


class ProductReview(AbstractBaseModel):
    product = ForeignKey('Product', on_delete=CASCADE, related_name='reviews')
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='reviews')
    body = TextField()
    rating = PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    like_count = PositiveIntegerField(default=0)


class ProductFavourite(AbstractBaseModel):
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='product_favourites')

    def __str__(self):
        return f'Favourite for {self.user.username} created on {self.created_at}'


class ProductFavouriteItem(AbstractBaseModel):
    product_favourite = ForeignKey('ProductFavourite', on_delete=CASCADE, related_name='item')
    product = ForeignKey('Product', on_delete=CASCADE, related_name='product_favourites')
    quantity = PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class ProductReviewFavourite(AbstractBaseModel):
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='product_review_favourites')

    def __str__(self):
        return f'Favourite for {self.user.username} created on {self.created_at}'


class ProductReviewFavouriteItem(AbstractBaseModel):
    product_review_favourite = ForeignKey('ProductReviewFavourite', on_delete=CASCADE, related_name='item')
    product_review = ForeignKey('ProductReview', on_delete=CASCADE, related_name='product_review_favourites')
    quantity = PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product_review.user.username}'s review"


class Cart(AbstractBaseModel):
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='carts')

    def __str__(self):
        return f'Cart for {self.user.username} created on {self.created_at}'


class CartItem(AbstractBaseModel):
    cart = ForeignKey('Cart', on_delete=CASCADE, related_name='items')
    product = ForeignKey('Product', on_delete=CASCADE, related_name='carts')
    quantity = PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price
