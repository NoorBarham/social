from django.urls import path, include
from .views import dashboard, profile_list, profile, register
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


app_name = "dwitter"

urlpatterns = [
    path("",dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    
    # change/reset password don't work, except when I added them explicitly here
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("dwitter:password_change_done")),
        name="password_change"),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("dwitter:password_reset_done")),
        name="password_reset"),    
]