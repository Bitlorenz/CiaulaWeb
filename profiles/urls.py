from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from profiles.views import UserCreateView, UserDetailView, UserUpdateView

app_name = 'profiles'

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user-registration"),
    path("<int:pk>/detail/", UserDetailView.as_view(), name="user-detail"),
    path("<int:pk>/update", UserUpdateView.as_view(), name="user-update"),
    path("login/", auth_views.LoginView.as_view(
        template_name='profiles/registration/login.html'
    ), name="user-login"),
    path("logout/", auth_views.LogoutView.as_view(
        template_name='profiles/registration/logged_out.html'
    ), name="user-logout"),
    path("change_password/", auth_views.PasswordChangeView.as_view(
        template_name='profiles/registration/change_password.html'),
        success_url=reverse_lazy('home'), name='change-password')
]
