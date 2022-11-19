from django.urls import path

from chat_app.views.auth_view import *
from rest_framework.authtoken import views

from chat_app.views.call_view import *
from chat_app.views.message_view import *

urlpatterns = [
    path('logout/', LogOutView.as_view()),
    path('message/', MessageView.as_view()),
    path('start-call/', StartCall.as_view()),
    path('end-call/', EndCall.as_view()),
    path('test-socket/', test_socket),
    path('my-chats/', MyChats.as_view()),
    path('message-create/', CreateMessageView.as_view()),
    path('message/with/<int:pk>/', MessageWithView.as_view()),
]
