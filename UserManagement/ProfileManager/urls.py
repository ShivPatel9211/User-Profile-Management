
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="login"),
    path('home/<str:userid>',views.home,name="home"),
    path('register',views.register,name="register"),
    path('resetPassword/', views.resetPassword,name='resetPassword'),
    path('postReset/', views.postReset,name='postReset'),
    path('logout/', views.logout, name="log"),
]
