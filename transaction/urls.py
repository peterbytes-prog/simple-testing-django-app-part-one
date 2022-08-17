from django.urls import path
import transaction.views as views

urlpatterns = [
    path('', views.index, name='index'),
]
