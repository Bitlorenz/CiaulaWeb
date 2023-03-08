
from ciaulaweb.views import UserCreateView


path("register/", UserCreateView.as_view(), name="register"),
