from django.urls import path

from .views import UserLoginView, UserRegisterView, UserLogoutView, UserLogoutConfirmView, UserUpdateView, \
    UserDetailView, FollowView, UnfollowView

app_name = 'users'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('logout/confirm/', UserLogoutConfirmView.as_view(), name='user-logout-confirm'),
    path('detail/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('update/<int:user_id>/', UserUpdateView.as_view(), name='user-update'),
    path('follow/', FollowView.as_view(), name='user-follow'),
    path('unfollow/', UnfollowView.as_view(), name='user-unfollow'),
]
