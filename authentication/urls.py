from django.urls import path
from .views import UserView, MyTokenObtainPairView, MyTokenRefreshView, LogoutView

urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('logout', LogoutView.as_view()),
    path('token/refresh', MyTokenRefreshView.as_view(), name='token_refresh'),
    # Register
    path('register', UserView.as_view()),
]
