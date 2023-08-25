from django.urls import path
from . import views

app_name = 'Accounts'

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path('login/', views.signin, name='signin'),
    path("logout/", views.signout, name="signout"),  
    path("internal/<int:pk>/homeint/", views.homeint, name="homeint"),
    path("internal/<int:pk>/homeprof/", views.homeprof, name="homeprof"),
    path("<int:pk>/coord/", views.coordination, name="coord"),
    path("internal/settings/", views.user_settings, name="settings"),
    path("internal/courses/", views.courses, name="courses"), 
    path('update_profile/', views.update_profile, name='update_profile'),

  
]
