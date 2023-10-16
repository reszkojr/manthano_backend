from django.urls import path

from . import views

urlpatterns = [
    # path('<int:classroom_code>/', views.classroom_home, name="classroom_home"),
    path('create/', views.CreateClassroom.as_view(), name='create_classroom'),
    # path('<slug:code>/', views.classroom, name='classroom'),
    # path('<slug:code>/<slug:channel>', views.classroom, name='classroom'),
]
