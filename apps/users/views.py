from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views import View

from .models import User, Follow, Feedback, UserCard
from .serializers import UserSerializer
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm, FeedbackCreateForm, FeedbackUpdateForm, \
    UserCardCreateForm, UserCardUpdateForm


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'users/user-login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'users/user-register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:user-login')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('home')


class UserLogoutConfirmView(View):
    template_name = 'users/user-logout-confirm.html'

    def get(self, request):
        return render(request, self.template_name)


class UserDetailView(View):
    template_name = 'users/user-detail.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, self.template_name, {'user': user})


class UserUpdateView(View):
    form_class = UserUpdateForm
    template_name = 'users/user-update.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form, 'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:user-detail', user_id=user.id)
        return render(request, self.template_name, {'form': form, 'user': user})


class FollowView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        if request.user != user_to_follow:
            Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        return redirect('users:user-detail', user_id=user_id)


class UnfollowView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
        return redirect('users:user-detail', user_id=user_id)


class FeedbackListView(View):
    template_name = 'users/feedback-list.html'

    def get(self, request):
        feedbacks = Feedback.objects.all()
        return render(request, self.template_name, {'feedbacks': feedbacks})


class FeedbackDetailView(View):
    template_name = 'users/feedback-detail.html'

    def get(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        return render(request, self.template_name, {'feedback': feedback})


class FeedbackCreateView(LoginRequiredMixin, View):
    form_class = FeedbackCreateForm
    template_name = 'users/feedback-create.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:feedback-list')
        return render(request, self.template_name, {'form': form})


class FeedbackDeleteView(LoginRequiredMixin, View):
    def post(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.delete()
        return redirect('users:feedback-list')


class FeedbackUpdateView(LoginRequiredMixin, View):
    form_class = FeedbackUpdateForm
    template_name = 'users/feedback-update.html'

    def get(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        form = self.form_class(instance=feedback)
        return render(request, self.template_name, {'form': form})

    def post(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        form = self.form_class(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('users:feedback-list')
        return render(request, self.template_name, {'form': form})


class UserCardCreate(LoginRequiredMixin, View):
    form_class = UserCardCreateForm
    template_name = 'users/user-card-create.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data['user'] = request.user
            form.save()
            return redirect('users:user-detail', request.user.id)
        return render(request, self.template_name, {'form': form})


class UserCardDeleteView(LoginRequiredMixin, View):
    def post(self, request, user_card_id):
        user_card = get_object_or_404(UserCard, id=user_card_id)
        user_card.delete()
        return redirect('users:user-detail', request.user.id)


class UserCardUpdateView(LoginRequiredMixin, View):
    form_class = UserCardUpdateForm
    template_name = 'users/user-card-update.html'

    def get(self, request, user_card_id):
        user_card = get_object_or_404(UserCard, id=user_card_id)
        form = self.form_class(instance=user_card)
        return render(request, self.template_name, {'form': form})

    def post(self, request, user_card_id):
        user_card = get_object_or_404(UserCard, id=user_card_id)
        form = self.form_class(request.POST, request.FILES, instance=user_card)
        if form.is_valid():
            form.cleaned_data['user'] = request.user
            form.save()
            return redirect('users:user-detail', request.user.id)
        return render(request, self.template_name, {'form': form})


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
