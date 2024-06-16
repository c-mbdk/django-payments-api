from django.urls import path, include
from .views import (
    AccountListApiView,
    AccountDetailApiView
)

urlpatterns = [
    path('api/', AccountListApiView.as_view(), name='accounts-list'),
    path('api/<int:id>/', AccountDetailApiView.as_view(), name='accounts-detail')
]