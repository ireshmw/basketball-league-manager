from django.urls import path

from api import views

urlpatterns = [
    path('dashboard', views.get_dashboard),
    path('games', views.get_all_games),
    path('teams/', views.get_teams),
    path('players/<int:pk>/', views.get_players_of_team, name='team-players'),
    path('player/<int:pk>/', views.get_player, name='single-player'),

    path('coach-team/<int:pk>/', views.get_team_of_coach, name='coach-team'),
    path('coach-players/<int:coach_id>/', views.get_players_of_coach),
    path('coach-players-above-avg/<int:coach_id>/', views.get_above_90_percentile_players_of_coach),

]
