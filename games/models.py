from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Console(models.Model):
    name = models.CharField(max_length=30)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=10)
    votes = models.IntegerField(default=0)
    console = models.ForeignKey(Console, on_delete=models.CASCADE)
    cover = models.CharField(max_length=250)
    igdb_id = models.IntegerField()

    def __str__(self):
        return str(self.name) + " - " + str(self.console)


class Vote(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " Voto por:  " + str(self.game)


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gamer_id = models.CharField(max_length=100, null=True)
    picture = models.CharField(max_length=250, default="None")
    games_owned = models.ManyToManyField(Game, related_name="games_owned", blank=True)
    games_wanted = models.ManyToManyField(Game, related_name="games_wanted", blank=True)

    def __str__(self):
        return self.user.username


class Exchange(models.Model):
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='exchange_creator')
    guest = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='exchange_guest')
    game_creator = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='exchange_game_creator')
    game_guest = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='exchange_game_guest')
    exchange_state = models.IntegerField(default=0)

    class Meta:
        ordering = ['exchange_state']

    def __str__(self):
        return str(self.creator) + ": tiene: " + str(self.game_creator) + " / " + str(self.guest) + ": tiene: " + str(
            self.game_guest)

