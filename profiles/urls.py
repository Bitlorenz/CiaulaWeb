from django.urls import path
from django.contrib.auth import views as auth_views
from profiles.views import UserCreateView

app_name = 'profiles'

urlpatterns = [
    path("register/", UserCreateView.as_view(template_name='profiles/user_create.html'), name="user-registration"),
    path("login/", auth_views.LoginView.as_view(
        template_name='profiles/registration/login.html'
    ), name="user-login"),
    path("logout/", auth_views.LogoutView.as_view(
        template_name='profiles/registration/logged_out.html'
    ), name="user-logout"),
]
