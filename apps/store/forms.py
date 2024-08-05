from django.forms import ModelForm

from .models import ProductReview


class ProductReviewCreateForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ('body',)


class ProductReviewUpdateForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ('body',)
