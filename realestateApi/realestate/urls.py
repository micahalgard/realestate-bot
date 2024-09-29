from django.urls import path

from . import views
app_name = 'realestate'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:property_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('create/submit', views.submit, name='submit')
]