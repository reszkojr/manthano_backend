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

    path('jitsi_channels/', views.GetClassroomJitsiChannelsView.as_view(), name='jitsi_channels_classroom'),
    path('jitsi_channel/add', views.AddJitsiChannelView.as_view(), name='jitsi_channel_add_classroom'),
    path('jitsi_channel/edit/<int:id>', views.UpdateJitsiChannelView.as_view(), name='jitsi_channel_edit_classroom'),
    path('jitsi_channel/delete/<int:id>', views.DeleteJitsiChannelView.as_view(), name='jitsi_channel_remove_classroom'),

    path('messages/', views.GetChannelMessagesView.as_view(), name='messages_classroom'),
    path('message/edit/<int:id>', views.UpdateMessageView.as_view(), name='message_edit_classroom'),
    path('message/delete/<int:id>', views.DeleteMessageView.as_view(), name='message_remove_classroom'),

    path('users', views.GetClassroomUsersView.as_view(), name='users_classroom')
    # path('<slug:code>/<slug:channel>', views.classroom, name='classroom'),
]
