from django.urls import path
from App import views_main
from App import views_api
from App import views_auth
from App import views_game

app_name="App"
urlpatterns = [
    path('', views_main.index),
    path('excel', views_main.excel, name='excel'),
    path('clear', views_main.clear, name='clear'),

    path('api/country/', views_api.get_all_default_countries),
    path('api/saved_games/', views_api.get_saved_games_of_user),
    path('api/delete_save/', views_api.delete_save_by_time),

    path('auth/registration/', views_auth.registration_in_system),
    path('auth/check_mail/', views_auth.check_email),
    path('auth/password_change/', views_auth.recovery_password),
    path('auth/login/', views_auth.try_login),
    path('auth/logout/', views_auth.try_logout),
    path('auth/recovery_password_code/', views_auth.recovery_password_code),

    path('game/start_game/', views_game.start_game, name='start_game'),
    path('game/load_game/', views_game.load_game, name='load_game'),
    path('game/save_game/', views_game.save_game, name='save_game'),
]
