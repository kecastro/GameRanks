from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django import forms
from django.contrib import messages
from django.db.models import Q

from .models import *
from .forms import *
from django.contrib.auth.models import User


# Create your views here.
class IndexView(ListView):
    template_name = 'games/index.html'
    context_object_name = 'top_3_games'
    queryset = Game.objects.order_by('-votes')[:3]


class AllGamesView(ListView):
    model = Game
    template_name = 'games/all_games.html'
    context_object_name = 'all_games'
    paginate_by = 10
    queryset = Game.objects.all().order_by('-votes')


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


def vote(request, game_id, user_id):
    u = get_object_or_404(User, pk=user_id)
    g = get_object_or_404(Game, pk=game_id)
    if Vote.objects.filter(user=u, game=g).exists():
        messages.error(request, "Solo se puede votar una vez por juego")
        return HttpResponseRedirect(reverse('games:game_view', kwargs={'pk': g.id}))
    else:
        if int(user_id) != int(request.user.id):
            messages.error(request, "Acesso restringido")
            return HttpResponseRedirect(reverse('games:game_view', kwargs={'pk': g.id}))
        else:
            v = Vote(game=g, user=u)
            v.save()
            g.votes += 1
            g.save()
            messages.success(request, "Gracias por votar")
            return HttpResponseRedirect(reverse('games:game_view', kwargs={'pk': g.id}))


def add_trade_games(request):
    user = User.objects.get(pk=request.user.id).useraccount

    if request.method == 'POST':
        owned_form = OwnedGamesForm(request.POST, instance=user)
        wanted_form = WantedGamesForm(request.POST, instance=user)

        if owned_form.is_valid() and wanted_form.is_valid():
            owned_form.save()
            wanted_form.save()

            return redirect('games:me')
        else:
            context = {
                "owned_form": OwnedGamesForm(instance=user),
                "wanted_form": WantedGamesForm(instance=user),
                "error_message": "Se debe seleccionar como minimo 1 juego de cada categoria (Ofrecer-Querer)"
            }

            return render(request, 'games/trade.html', context)

    context = {
        "owned_form": OwnedGamesForm(instance=user),
        "wanted_form": WantedGamesForm(instance=user),
    }

    return render(request, 'games/trade.html', context)


def generate_exchange(request):

    user = get_object_or_404(User, username=request.user.username)

    if request.method == "POST":
        creator = User.objects.get(pk=int(request.POST.get("creator").strip()))
        guest = User.objects.get(pk=int(request.POST.get("guest").strip()))
        creator_game = Game.objects.get(pk=int(request.POST.get("creator_game").strip()))
        guest_game = Game.objects.get(pk=int(request.POST.get("guest_game").strip()))
        creator.useraccount.games_owned.remove(creator_game)
        creator.useraccount.games_wanted.remove(guest_game)
        Exchange.objects.create(creator=creator.useraccount, guest=guest.useraccount, game_creator=creator_game,
                                game_guest=guest_game)
        return redirect('games:me')
    else:
        context = {}
        response = {}
        exchangeObject = {}
        key = 0
        for otherUser in UserAccount.objects.all():
            for myGame in user.useraccount.games_owned.all():
                if myGame in otherUser.games_wanted.all():
                    for otherGame in otherUser.games_owned.all():
                        if otherGame in user.useraccount.games_wanted.all():
                            exchangeObject = {}
                            exchangeObject['creator'] = user
                            exchangeObject['guest'] = otherUser.user
                            exchangeObject['creatorGame'] = myGame
                            exchangeObject['guestGame'] = otherGame

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
                state = int(request.POST.get("state").strip())
                if exchange.exchange_state == 0:
                    exchange.exchange_state = state
                    exchange.save()
                    context["message"] = "Gracias por completar el proceso de intercambio"
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