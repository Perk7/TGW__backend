from django.urls import path
from App import views_main
from App import views_api
from App import views_auth
from App import views_game
from django.conf.urls import url

app_name="App"
urlpatterns = [
    path('', views_main.index),
    path('excel', views_main.excel, name='excel'),
    path('clear', views_main.clear, name='clear'),

    url('api/country/', views_api.get_all_default_countries),
    url('api/saved_games/', views_api.get_saved_games_of_user),
    url('api/delete_save/', views_api.delete_save_by_time),

    url('auth/registration', views_auth.registration_in_system),
    url('auth/check_mail', views_auth.check_email),
    url('auth/password_change', views_auth.recovery_password),
    url('auth/login', views_auth.try_login),
    url('auth/logout', views_auth.try_logout),
    url('auth/recovery_password_code', views_auth.recovery_password_code),

    url('game/start_game/', views_game.start_game, name='start_game'),
    url('game/load_game/', views_game.load_game, name='load_game'),
    url('game/save_game/', views_game.save_game, name='save_game'),
]
