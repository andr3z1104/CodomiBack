from django.contrib import admin
from django.urls import path
from login import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin/', admin.site.urls),
]
