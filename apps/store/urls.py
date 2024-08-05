from django.urls import path

from .views import CartView, AddToCartView, RemoveFromCartView, UpdateCartView, \
    ProductFavouriteView, AddToProductFavouriteView, RemoveFromProductFavouriteView, UpdateProductFavouriteView, \
    ProductReviewListView, ProductReviewUpdateView, ProductReviewCreateView, ProductDetailView, ProductListView

app_name = 'store'
urlpatterns = [
    # cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:product_id>', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/update/<int:product_id>', UpdateCartView.as_view(), name='update-cart'),

    # product-favourite
    path('product_favourite/', ProductFavouriteView.as_view(), name='product-favourite'),
    path('product_favourite/add/<int:product_id>', AddToProductFavouriteView.as_view(),
         name='add-to-product-favourite'),
    path('product_favourite/remove/<int:product_id>', RemoveFromProductFavouriteView.as_view(),
         name='remove-from-product-favourite'),
    path('product_favourite/update/<int:product_id>', UpdateProductFavouriteView.as_view(),
         name='update-product-favourite'),

    # product
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/detail/<int:product_id>', ProductDetailView.as_view(), name='product-detail'),

    # product-review
    path('reviews/', ProductReviewListView.as_view(), name='product-review-list'),
    path('reviews/create/', ProductReviewCreateView.as_view(), name='product-review-create'),
    path('reviews/<int:pk>/update/', ProductReviewUpdateView.as_view(), name='product-review-update'),
]
