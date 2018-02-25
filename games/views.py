import urllib

import simplejson
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.http import QueryDict
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django import forms
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail


from .models import *
from .tasks import *
from .forms import *
from django.contrib.auth.models import User

import json, datetime


# Create your views here.
class IndexView(ListView):
    template_name = 'games/index.html'
    context_object_name = 'top_10_games'
    best_games = Game.objects.order_by('-rating')
    queryset = best_games.filter(release__year=2018)[:10]


class GameView(DetailView):
    template_name = 'games/game.html'
    model = Game


class UserView(DetailView):
    template_name = 'games/user_page.html'
    model = User
    context_object_name = 'other_user'
    slug_field = 'username'


class CurrentUserView(DetailView):
    template_name = 'games/me.html'
    context_object_name = 'me'
    def get_object(self):
        return self.request.user

def register(request):
    form_extra = UserProfileForm(request.POST or None, prefix='userprofile')
    form = UserForm(request.POST or None, prefix='user')

    if form.is_valid() and form_extra.is_valid():
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            form.add_error("email", "Correo ya existe")
        else:
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            useraccount = form_extra.save(commit=False)
            useraccount.user = user
            useraccount.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('games:index')
    context = {
        "form": form,
        "form_extra": form_extra,
    }
    return render(request, 'games/register.html', context)

def edit_user(request):
    u = get_object_or_404(User, pk=request.user.id)
    old_email = u.email
    form_extra = UserProfileForm(request.POST or None, prefix='userprofile', instance=u.useraccount)
    form = UserForm(request.POST or None, prefix='user', instance=u)

    if form.is_valid() and form_extra.is_valid():
        email = form.cleaned_data['email']
        if old_email != email:
            if User.objects.filter(email=email).exists():
                form.add_error("email", "Correo ya existe")
            else:
                u = form.save(commit=False)
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                u.set_password(password)
                u.save()
                useraccount = form_extra.save(commit=False)
                useraccount.user = u
                useraccount.save()

                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('games:me')
        else:
            u = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            u.set_password(password)
            u.save()
            useraccount = form_extra.save(commit=False)
            useraccount.user = u
            useraccount.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('games:me')

    context = {
        "form": form,
        "form_extra": form_extra,
    }
    return render(request, 'games/edit_user.html', context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('games:index'))


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if not request.POST.get('remember', None):
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)
                return redirect('games:index')
            else:
                return render(request, 'games/login.html', {'error_message': 'Cuenta suspendida'})
        else:
            return render(request, 'games/login.html', {'error_message': 'Usuario y/o contraseña incorrectos'})
    return render(request, 'games/login.html')


def getSearchGames(request, query):
    if request.user.is_authenticated():
        games = json.dumps([g.get_json() for g in Game.objects.filter(name__icontains=query)])
        return HttpResponse(games)
    else:
        return HttpResponseBadRequest()

def add_trade_games(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            for game in simplejson.loads(request.body):
                g = get_object_or_404(Game, pk=game["id"])
                if len(request.user.useraccount.trading_user.filter(Q(game=g) & Q(platform=game["platform"]))) <= 0:
                    trade = TradeOption.objects.create(game=g, user=request.user.useraccount, type=game["type"], platform=game["platform"])
            return HttpResponse()
        return render(request, 'games/trade.html')
    else:
        return redirect('games:login')

def add_game(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            from igdb_api_python.igdb import igdb
            igdb = igdb("dfd4b285e76c0d3f97a549b2edd9467e")
            context = {}
            if request.POST['action'] == "search":
                possible_games = {}
                consoles = [9,12,37,41,46,48,49]
                result = igdb.games({
                    'search': request.POST['query'],
                    'limit': 50,
                    'fields': ['name', 'release_dates', 'cover']
                })
                for game in result.body:
                    if "release_dates" in game:
                        can_add = False
                        for platforms in game["release_dates"]:
                            if platforms['platform'] in consoles:
                                can_add = True
                        if can_add:
                            possible_games[game["id"]] = {"id": game["id"], "name": game["name"], "cover": game["cover"]["url"][2:] if "cover" in game else None}
                context["possible_games"] = possible_games
                context["not_found"] = True
                return render(request, 'games/add_game.html', context)
            elif request.POST['action'] == "add":
                g = Game.objects.filter(igdb=request.POST['game_id'])
                if g.exists():
                    context["message"] = "El juego ya existe en la base de datos"
                    context["game_id"] = g[0].id
                else:
                    consoles_id = {"9":"PlayStation 3", "12":"Xbox 360", "37":"Nintendo 3DS", "41":"Wii U", "46":"PlayStation Vita", "48":"PlayStation 4", "49":"Xbox One"}
                    result = igdb.games({
                        'ids': int(request.POST['game_id']),
                        'fields': ['name','release_dates', 'cover', 'screenshots', 'first_release_date', 'aggregated_rating']
                    })
                    for game in result.body:


                        tmp_s = game["screenshots"] if "screenshots" in game else None

                        screenshots = ""

                        if tmp_s != None:
                            for s in tmp_s:
                                url = s["url"][2:]
                                screenshots += url.replace("t_thumb", "t_original") + ","
                            screenshots = screenshots[:-1]
                        else:
                            screenshots = None

                        tmp_p = game["release_dates"] if "release_dates" in game else None

                        platforms = ""

                        duplicate_regions = []

                        if tmp_p != None:
                            for p in game["release_dates"]:
                                if str(p["platform"]) in consoles_id and str(p["platform"]) not in duplicate_regions:
                                    platforms += consoles_id[str(p["platform"])] + ","
                                    duplicate_regions.append(str(p["platform"]))
                            platforms = platforms[:-1]

                        new_game = Game.objects.create(igdb=game["id"],
                                                       name=game["name"],
                                                       rating=game["aggregated_rating"] if "aggregated_rating" in game else None,
                                                       release=datetime.datetime.fromtimestamp(int(game["first_release_date"]/1000)).strftime('%Y-%m-%d') if "first_release_date" in game else None,
                                                       screenshots=screenshots,
                                                       cover=game["cover"]["url"][2:].replace("t_thumb", "t_original") if "cover" in game else None,
                                                       platform=platforms)
                        context["message"] = "Juego agregado existosamente"
                        context["game_id"] = new_game.id
                return render(request, 'games/add_game.html', context)
        return render(request, 'games/add_game.html')
    else:
        return redirect('games:login')


def generate_exchange(request):

    if request.method == "POST":
        creator = User.objects.get(pk=int(request.POST.get("creator").strip()))
        guest = User.objects.get(pk=int(request.POST.get("guest").strip()))
        creator_game = Game.objects.get(pk=int(request.POST.get("creator_game").strip()))
        creator_platform = request.POST.get("creator_platform").strip()
        guest_game = Game.objects.get(pk=int(request.POST.get("guest_game").strip()))
        guest_platform = request.POST.get("guest_platform").strip()

        e = Exchange.objects.create(creator=creator.useraccount, guest=guest.useraccount, game_creator=creator_game,
                                creator_platform=creator_platform,game_guest=guest_game, guest_platform=guest_platform)

        message_guest = 'El usuario ' + str(creator.username) + ' ha generado un intercambio, visita tu perfil para verlo'
        email('Intercambio generado', message_guest, 'soporte-gameranks@outlook.com', guest.email)

        data = {
            'm': 'Cambio generado exitosamente',
            'e': e.id
        }

        return redirect('games:me')
    else:
        user = get_object_or_404(User, username=request.user.username)
        context = {}
        response = {}
        exchangeObject = {}
        key = 0

        for wanttrade in user.useraccount.trading_user.filter(type=True):
            for trade in TradeOption.objects.filter(~Q(user=user.useraccount) & Q(type=False) & Q(game=wanttrade.game) & Q(platform=wanttrade.platform)):
                for otherwant in trade.user.trading_user.filter(type=True):
                    for offertrade in user.useraccount.trading_user.filter(Q(type=False) & Q(game=otherwant.game) & Q(platform=otherwant.platform)):
                        exchangeObject = {}
                        exchangeObject['creator'] = user
                        exchangeObject['guest'] = otherwant.user.user
                        exchangeObject['creatorGame'] = offertrade.game
                        exchangeObject['creatorPlatform'] = offertrade.platform
                        exchangeObject['guestGame'] = wanttrade.game
                        exchangeObject['guestPlatform'] = wanttrade.platform

                        response[str(key)] = exchangeObject
                        key += 1

        if len(response) > 0:
            context["response"] = response
        else:
            context["message"] = "No hay posibles cambios por el momento"
    return render(request, 'games/exchange.html', context)

def exchange_view(request, exchange_id):
    exchange = get_object_or_404(Exchange, pk=exchange_id)
    context ={}
    if request.user.is_authenticated():
        if int(request.user.id) == int(exchange.creator.user.id) or int(request.user.id) == int(exchange.guest.user.id):
            if request.method == "POST":
                if 'accept' in request.POST:
                    accept = int(request.POST.get("accept").strip())
                    if accept == 1:
                        exchange.accepted = True
                        exchange.save()
                    else:
                        exchange.accepted = False
                        exchange.exchange_state = 2
                        exchange.save()
                elif 'state' in request.POST:
                    state = int(request.POST.get("state").strip())
                    if exchange.exchange_state == 0:
                        exchange.exchange_state = state
                        exchange.save()
                        context["message"] = "Gracias por completar el proceso de intercambio"
                        if state == 1 and exchange.accepted is True: #Cambio completado
                            creator = User.objects.get(pk=exchange.creator.user.id)
                            guest = User.objects.get(pk=exchange.guest.user.id)

                            creator.useraccount.trading_user.filter(Q(game=exchange.game_creator) & Q(type=False)).delete()
                            creator.useraccount.trading_user.filter(Q(game=exchange.game_guest) & Q(type=True)).delete()
                            guest.useraccount.trading_user.filter(Q(game=exchange.game_guest) & Q(type=False)).delete()
                            guest.useraccount.trading_user.filter(Q(game=exchange.game_creator) & Q(type=True)).delete()

                            #if exchange is completed, all pending exchanges that have
                            #the games from the completed exchange, will be terminated
                            for x in creator.useraccount.exchange_creator.all():
                                if x.game_creator.id == exchange.game_creator.id:
                                    if x.exchange_state == 0:
                                        x.exchange_state = 2
                                        x.save()
                            for x in creator.useraccount.exchange_guest.all():
                                if x.game_guest.id == exchange.game_creator.id:
                                    if x.exchange_state == 0:
                                        x.exchange_state = 2
                                        x.save()
                            for x in guest.useraccount.exchange_guest.all():
                                if x.game_guest.id == exchange.game_guest.id:
                                    if x.exchange_state == 0:
                                        x.exchange_state = 2
                                        x.save()
                            for x in guest.useraccount.exchange_creator.all():
                                if x.game_creator.id == exchange.game_guest.id:
                                    if x.exchange_state == 0:
                                        x.exchange_state = 2
                                        x.save()
            context["exchange"] = exchange
        else:
            context = {
                "error_message": "No tiene acceso"
            }
    else:
        context["error_message"] = "Por favor inicie sesion"
    return render(request, 'games/detail_exchange.html', context)


def search_game(request):
    query = request.GET.get('query')
    if query is not None and query != '' and request.is_ajax():
        games = Game.objects.filter(Q(name__icontains=query))[:10]
        return render(request, 'games/game_search.html', {'games': games})
    return render(request, 'games/game_search.html')

def search_user(request):
    query = request.GET.get('query')
    if query is not None and query != '' and request.is_ajax():
        usernames = User.objects.filter(Q(username__icontains=query))[:10]
        return render(request, 'games/user_search.html', {'users':usernames})
    return render(request, 'games/user_search.html')

def remove_trade(request, trade_id):
    if request.user.is_authenticated():
        trade = get_object_or_404(TradeOption, pk=trade_id)
        if trade.user == request.user.useraccount:
            trade.delete()
            return redirect('games:trade')
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()

def contact(request):
    if request.method == 'POST':
        message = request.POST.get("message")
        name = "Nombre: " + str(request.POST.get("name"))
        mail = "Correo: " + str(request.POST.get("email"))

        m = "\n".join([name, ' ', mail, ' ', message])

        email('Mensaje enviado', m, 'soporte-gameranks@outlook.com', mail)

        data = {
            'm': 'Mensaje enviado satisfactoriamente'
        }

        return render(request, 'games/contact.html', data)
    return render(request, 'games/contact.html')

def about(request):
    return render(request, 'games/about.html')

def help(request):
    return render(request, 'games/help.html')
