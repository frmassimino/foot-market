from django.db import models
from player.models import Player
from user.models import CustomUser, Portfolio
#from django.contrib.auth.models import User

# Create your models here.



class Ipo(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    start_price = models.IntegerField(default=0)
    ipo_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='Open')

    def __str__(self):
        return(self.player.get_name())

    def ipo_close(self,amount):
        self.player.expand_pool(amount)
        self.player.save()
        self.status = 'Closed'
        self.save()
    
    def get_ipo_player(self):
        return self.player

    def get_ipo_count(self):
        return self.ipo_count

    def get_ipo_status(self):
        return self.status

class Bidder(models.Model):
    id = models.AutoField(primary_key=True)
    bidder = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    ipo = models.ForeignKey(Ipo, on_delete=models.SET_NULL, null=True, blank=False)
    value = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='Set')
    value_last = models.IntegerField(default=0)
    value_actual = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=False)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=False)

    def check_funds(self, user):
        if (user.funds - self.value) >= 0:
            return True
        else:
            return False

    def bidder_close(self):
        self.status = 'Lost'
        self.bidder.set_funds_variation(self.value)
        self.save()
    
    def bidder_cancel(self):
        self.status = 'Canceled'
        self.save()

    def bidder_close_winner(self):
        portfolio, created = Portfolio.objects.get_or_create(user=self.bidder, player=self.ipo.get_ipo_player())
        portfolio.add_count()
        portfolio.save()
        self.bidder.set_funds_variation(-(self.value))
        self.status = 'Won'
        self.save()

    def get_value_actual(self):
        return self.value_actual


