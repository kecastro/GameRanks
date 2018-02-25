from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

CONSOLES = (
    ("Xbox One", "Xbox One"),
    ("Xbox 360", "Xbox 360"),
    ("PlayStation 4", "PlayStation 4"),
    ("PlayStation 3", "PlayStation 3"),
    ("PlayStation Vita", "PlayStation Vita"),
    ("Wii U", "Wii U"),
    ("Nintendo 3DS", "Nintendo 3DS")
)

class Game(models.Model):
    igdb = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    rating = models.FloatField(null=True)
    release = models.DateField(null=True)
    screenshots = models.CharField(max_length=2000, null=True)
    cover = models.CharField(max_length=1000, null=True)
    platform = models.CharField(max_length=500)

    def __str__(self):
        return str(self.name)

    def screenshots_as_list(self):
        if self.screenshots != None:
            return self.screenshots.split(',')

    def platforms_as_list(self):
        if self.platform != None:
            return self.platform.split(',')

    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "cover": self.cover,
            "platforms": self.platform.split(',')
        }


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gamer_id = models.CharField(max_length=100, null=True)
    picture = models.CharField(max_length=250, default="None")
    phone = models.CharField(max_length=15, default="(000)000-0000")
    city = models.CharField(max_length=30, default="Colombia")

    def __str__(self):
        return self.user.username

class Exchange(models.Model):
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='exchange_creator')
    guest = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='exchange_guest')
    game_creator = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='exchange_game_creator')
    creator_platform = models.CharField(max_length=30, choices=CONSOLES)
    game_guest = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='exchange_game_guest')
    guest_platform = models.CharField(max_length=30, choices=CONSOLES)
    exchange_state = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['exchange_state']

    def __str__(self):
        return str(self.creator) + ": tiene: " + str(self.game_creator) + " / " + str(self.guest) + ": tiene: " + str(
            self.game_guest)


class TradeOption(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tradable_game')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='trading_user')
    type = models.BooleanField() #True = Quiero #False = Ofrezco
    platform = models.CharField(max_length=30, choices=CONSOLES)

    def __str__(self):
        return self.game.name + " - " + self.user.user.username