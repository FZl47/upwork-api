from django.urls import path

from . import views

app_name = 'apps.account'
urlpatterns = [
    path('signup/<str:role>', views.Signup.as_view(), name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),

    path('token/refresh/', views.TokenRefresh.as_view(), name='token_refresh'),
]
