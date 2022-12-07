from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include("dwitter.urls")),
    
    #password_reset_confirm works when i put the path here
    path(
        'password_reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('dwitter:password_reset_complete')),
        name="password_reset_confirm",
    ),
    # need to rewrite the password_reset path here if I want to put an email that is not in the database
]
