from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import Cart, Product, CartItem, ProductFavourite, ProductFavouriteItem, ProductReview, Product, \
    ProductReviewFavourite, ProductReviewFavouriteItem

from .forms import ProductReviewUpdateForm, ProductReviewCreateForm


# -------------------- Product --------------------

class ProductListView(View):
    template_name = 'store/product-list.html'

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        return render(request, self.template_name, {'products': products})


class ProductDetailView(View):
    template_name = 'store/product-detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, self.template_name, {'product', product})


# -------------------- Product --------------------

class ProductReviewListView(View):
    template_name = 'store/product-review-list.html'

    def get(self, request):
        product_reviews = ProductReview.objects.all()
        return render(request, self.template_name, {'product-reviews': product_reviews})


class ProductReviewDetailView(View):
    template_name = 'store/product-review-detail.html'

    def get(self, request, product_review_id):
        product_review = get_object_or_404(ProductReview, id=product_review_id)
        return render(request, self.template_name, {'product-review': product_review})


class ProductReviewCreateView(View):
    form_class = ProductReviewCreateForm
    template_name = 'store/product-review-create.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form', form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:product-review-list')
        return render(request, self.template_name, {'form': form})


class ProductReviewUpdateView(View):
    form_class = ProductReviewUpdateForm
    template_name = 'store/product-review-update.html'

    def get(self, request, product_review_id):
        product_review = get_object_or_404(ProductReview, id=product_review_id)
        form = self.form_class(instance=product_review)
        return render(request, self.template_name, {'form': form})

    def post(self, request, product_review_id):
        product_review = get_object_or_404(ProductReview, id=product_review_id)
        form = self.form_class(request.POST, instance=product_review)
        if form.is_valid():
            form.save()
            return redirect('store:product-review-list')
        return render(request, self.template_name, {'form': form})


# -------------------- Cart --------------------
class CartView(LoginRequiredMixin, View):
    template_name = 'store/cart.html'

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'cart': cart})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('store:cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return redirect('store:cart')


class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        quantity = int(request.POST.get('quantity', 0))
        cart_item = get_object_or_404(CartItem, id=item_id)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('store:cart')


# -------------------- ProductFavourite --------------------
class ProductFavouriteView(LoginRequiredMixin, View):
    template_name = 'store/product-favourite.html'

    def get(self, request):
        product_favourite, created = ProductFavourite.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'product-favourite': product_favourite})


class AddToProductFavouriteView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product_favourite, created = ProductFavourite.objects.get_or_create(user=request.user)
        product_favourite_item, created = ProductFavouriteItem.objects.get_or_create(
            product_favourite=product_favourite, product=product)
        if not created:
            product_favourite_item.quantity += 1
            product_favourite_item.save()
        return redirect('store:product-favourite')


class RemoveFromProductFavouriteView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        product_favourite_item = get_object_or_404(ProductFavouriteItem, id=item_id)
        product_favourite_item.delete()
        return redirect('store:product-favourite')


class UpdateProductFavouriteView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        quantity = int(request.POST.get('quantity', 0))
        product_favourite_item = get_object_or_404(ProductFavouriteItem, id=item_id)
        if quantity > 0:
            product_favourite_item.quantity = quantity
            product_favourite_item.save()
        else:
            product_favourite_item.delete()
        return redirect('store:product-favourite')


# -------------------- ProductReviewFavourite --------------------
class ProductReviewFavouriteView(LoginRequiredMixin, View):
    template_name = 'store/product-review-favourite.html'

    def get(self, request):
        product_review_favourite, created = ProductReviewFavourite.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'product-review-favourite': product_review_favourite})


class AddToProductReviewFavouriteView(LoginRequiredMixin, View):
    def post(self, request, product_review_id):
        product_review = get_object_or_404(ProductReview, id=product_review_id)
        product_review_favourite, created = ProductReviewFavourite.objects.get_or_create(user=request.user)
        product_review_favourite_item, created = ProductReviewFavouriteItem.objects.get_or_create(
            product_review_favourite=product_review_favourite, product_review=product_review
        )
        if not created:
            product_review_favourite_item.quantity += 1
            product_review_favourite_item.save()
        return redirect('store:product-review-favourite')


class RemoveFromProductReviewView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        product_review_favourite_item = get_object_or_404(ProductReviewFavouriteItem, id=item_id)
        product_review_favourite_item.delete()
        return redirect('store:product-review-favourite')


class UpdateProductReviewView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        quantity = int(request.POST.get('quantity', 0))
        product_review_favourite_item = get_object_or_404(ProductReviewFavouriteItem, id=item_id)
        if quantity > 0:
            product_review_favourite_item.quantity = quantity
            product_review_favourite_item.save()
        else:
            product_review_favourite_item.delete()
        return redirect('store:product-review-favourite')
