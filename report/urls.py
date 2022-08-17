from django.urls import path
import report.views as views

urlpatterns = [
    path('', views.index, name='index'),
]
