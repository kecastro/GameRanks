from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^all/$', views.AllGamesView.as_view(), name='all_games'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^trade/$', views.add_trade_games, name='trade'),
    url(r"^user/current/$", views.CurrentUserView.as_view(), name="me"),
    url(r"^user/current/edit/$", views.edit_user, name="edit_me"),
    url(r'^user/current/exchange$', views.generate_exchange, name='generate_exchange'),
    url(r'^exchange/(?P<exchange_id>[0-9]+)/$', views.exchange_view, name='exchange_view'),
    url(r'^user/(?P<slug>[a-zA-Z0-9]+)/$', views.UserView.as_view(), name='users_page'),
    url(r'^(?P<pk>[0-9]+)/$', views.GameView.as_view(), name='game_view'),
    url(r'^(?P<game_id>[0-9]+)/(?P<user_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^search/$', views.search_game, name='search_game'),
    url(r'^searchuser/$', views.search_user, name='search_user'),
    url(r'^contact/$', views.contact, name='contact'),
]