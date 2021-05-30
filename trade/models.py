from django.db import models
from user.models import CustomUser, Portfolio
from player.models import Player
# Create your models here.


class Trade(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.OneToOneField(Player, on_delete=models.SET_NULL, primary_key=False, null=True)

    def __str__(self):
        return ('{0} {1}'.format(self.player.name, self.player.surname))

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    #trade = models.ForeignKey(Trade, on_delete=models.SET_NULL, null=True, blank=False)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, primary_key=False, null=True)
    value = models.IntegerField(default=0)
    value_last = models.IntegerField(default=0)
    value_actual = models.IntegerField(default=0)
    status = models.CharField(max_length=120, null=False, blank=False, default = 'Set')
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return (str(self.value)+' - '+self.owner.username)

    def bid_close(self):
        self.status = 'Done'
        self.save()
    
    def bid_cancel(self):
        self.status = 'Canceled'
        self.save()

    def bid_set_value(self, value):
        self.value = value
        self.save()

class Ask(models.Model):
    id = models.AutoField(primary_key=True)
    #trade = models.ForeignKey(Trade, on_delete=models.SET_NULL, null=True, blank=False)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, primary_key=False, null=True)
    value = models.IntegerField(default=0)
    status = models.CharField(max_length=120, null=False, blank=False, default = 'Set')
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=False)
    #owner = models.CharField(max_length=120,blank = False)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=False)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=False)

    def __str__(self):
        return (str(self.value)+' - '+self.owner.username)

    def ask_close(self):
        self.status = 'Done'
        self.save()
    
    def ask_cancel(self):
        portfolio = Portfolio.objects.get(user=self.owner, player=self.player)
        portfolio.sub_compromised()
        portfolio.sub_count()
        self.status = 'Canceled'
        self.save()

    def ask_set_value(self, value):
        self.value = value
        self.save()

class SuccessTrade(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField(default=0)
    bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, null=True, blank=False)
    ask = models.ForeignKey(Ask, on_delete=models.SET_NULL, null=True, blank=False)
