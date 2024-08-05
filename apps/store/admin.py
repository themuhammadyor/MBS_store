from django.contrib import admin

from .models import Cart, Product, CartItem, ProductFavourite, ProductFavouriteItem, ProductReview, \
    ProductReviewFavourite, ProductReviewFavouriteItem, Category, SubCategory, Brand, Discount


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductFavourite)
class ProductFavouriteAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductFavouriteItem)
class ProductFavouriteItemAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductReviewFavourite)
class ProductReviewFavouriteAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductReviewFavouriteItem)
class ProductReviewFavouriteItemAdmin(admin.ModelAdmin):
    pass
