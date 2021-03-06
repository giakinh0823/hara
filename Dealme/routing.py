from django.urls import path

from Dealme import consumers

ws_urlpatterns = [
    path('ws/products/', consumers.ProductsConsumer.as_asgi()),
    path('ws/comment/<str:room_name>/', consumers.CommentsConsumer.as_asgi()),
    path('ws/notify/<str:room_name>/', consumers.NotifierConsumer.as_asgi()),
    path('ws/order/<str:room_name>/', consumers.OrderConsumer.as_asgi()),
    path('ws/message/<str:room_name>/', consumers.MessageConsumer.as_asgi()),

]