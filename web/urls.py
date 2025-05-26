from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('category/', views.category, name='category'),
    path('characters/<str:name>/', views.characters, name="characters"),
    path('characters/<str:category>/<str:name>/', views.characterDetails, name='characterDetails'),
    path('search/', views.search_character, name='search_character'),
]

