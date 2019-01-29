from django.urls import path
from lpr import views

app_name = 'lpr'

urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('list', views.ListView.as_view(), name='list'),
    path('result', views.FinalView.as_view(), name='listresult'),
]