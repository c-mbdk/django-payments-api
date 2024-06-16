from django.urls import path, include
from .views import (
    TransactionListApiView,
    TransactionDetailApiView
)

urlpatterns = [
    path('api/', TransactionListApiView.as_view(), name='transactions-list'),
    path('api/<int:id>/', TransactionDetailApiView.as_view(), name='transactions-detail')
]