from django.conf.urls import url

from . import views

app_name = "games"
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^trade/$', views.add_trade_games, name='trade'),
    url(r"^user/current/$", views.CurrentUserView.as_view(), name="me"),
    url(r"^user/current/edit/$", views.edit_user, name="edit_me"),
    url(r'^user/current/exchange/$', views.generate_exchange, name='generate_exchange'),
    url(r'^exchange/(?P<exchange_id>[0-9]+)/$', views.exchange_view, name='exchange_view'),
    url(r'^remove_trade/(?P<trade_id>[0-9]+)/$', views.remove_trade, name='remove_trade'),
    url(r'^user/(?P<slug>[a-zA-Z0-9]+)/$', views.UserView.as_view(), name='users_page'),
    url(r'^(?P<pk>[0-9]+)/$', views.GameView.as_view(), name='game_view'),
    url(r'^search/$', views.search_game, name='search_game'),
    url(r'^searchuser/$', views.search_user, name='search_user'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_game/$', views.add_game, name='add_game'),
    url(r'^help/$', views.help, name='help'),
    url(r'^tradesearch/(?P<query>[\w|\W]+)$', views.getSearchGames, name='game_trade_search'),
]