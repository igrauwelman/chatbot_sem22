from django.urls import path
from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('chat/<int:chatid>', Index.as_view(), name='index_chatid'),
]