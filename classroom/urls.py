from django.urls import path

from . import views

urlpatterns = [
    # path('<int:classroom_code>/', views.classroom_home, name="classroom_home"),
    path('create/', views.CreateClassroomView.as_view(), name='create_classroom'),
    path('join/', views.JoinClassroomView.as_view(), name='join_classroom'),
    path('user/', views.GetUserClassroomView.as_view(), name='user_classroom'),

    path('channels/', views.GetClassroomChannelsView.as_view(), name='channels_classroom'),
    path('channel/add', views.AddChannelView.as_view(), name='channel_add_classroom'),
    path('channel/edit/<int:id>', views.UpdateChannelView.as_view(), name='channel_edit_classroom'),
    path('channel/delete/<int:id>', views.DeleteChannelView.as_view(), name='channel_remove_classroom'),

    path('messages/', views.GetChannelMessagesView.as_view(), name='messages_classroom'),
    # path('<slug:code>/<slug:channel>', views.classroom, name='classroom'),
]
