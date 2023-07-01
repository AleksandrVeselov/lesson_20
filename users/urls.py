
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, generate_new_password, activate_new_user

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),  # http://127.0.0.1:8000/users/
    path('logout/', LogoutView.as_view(), name='logout'),  # http://127.0.0.1:8000/users/logout
    path('register/', RegisterView.as_view(), name='register'),  # http://127.0.0.1:8000/users/register
    path('profile/', ProfileView.as_view(), name='profile'),  # http://127.0.0.1:8000/users/profile

    # http://127.0.0.1:8000/users/profile/genpassword
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    # http://127.0.0.1:8000/users/activate/<pk>
    path('activate/<int:pk>/', activate_new_user, name='activate_new_user')
]