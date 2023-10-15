from django.urls import path

from . import views

urlpatterns = [
    path('<int:classroom_code>/', views.classroom_home, name="classroom_home")
]
