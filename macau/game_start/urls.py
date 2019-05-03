from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('new', views.new_game, name="New game"),
    path('j/<int:game_pin>', views.join_game_by_url, name="Join game"),
    path('join', views.join_game_by_pin),
]
