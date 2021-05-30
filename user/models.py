from django.db import models
#from django.conf import settings
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from player.models import Player

from .managers import CustomUserManager
# Create your models here.
#User = get_user_model()

class CustomUser(AbstractUser):
    #username = models.CharField(max_length=40, unique=True)
    #email = models.EmailField(_('email address'), unique=True)
    age = models.IntegerField(default=0)
    funds = models.IntegerField(default=0)

    #objects = CustomUserManager()

    #USERNAME_FIELD = 'username'
    #EMAIL_FIELD = 'email'
    #REQUIRED_FIELDS = ['email']

    def __str__(self):
        return (f'{self.username}')

    def get_funds(self):
        return self.funds   

    def set_funds_variation(self, amount):
        self.funds = self.funds + amount
        self.save()

    def get_user(self):
        return self

#if i have to lookup for a model and the foreign key is in the other model, i just have to: 'portfolio_set' instead of the model -> queryset
class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=False)
    count = models.IntegerField(default = 0)
    compromised = models.IntegerField(default = 0)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=False)
    #value_total = models.IntegerField(default=get_value_total())

    def add_count(self):
        self.count = self.count + 1
        self.save()

    def sub_count(self):
        if (self.count - self.compromised - 1) < 0:
            raise ValueError("You don't have enough assets.")
        else:
            self.count = self.count - 1
            self.save()
    
    def check_count(self):
        if (self.count - self.compromised - 1) < 0:
            return False
        else:
            return True

    def add_compromised(self):
        self.compromised = self.compromised + 1
        self.save()

    def sub_compromised(self):
        self.compromised = self.compromised - 1
        self.save()

    def get_value_total(self):
        return self.player.price_actual*self.count

    def get_value_actual(self):
        return self.player.price_actual
    
    def get_value_last(self):
        return self.player.price_last

    def get_value_percentege(self):
        return ((self.player.price_actual-self.player.price_last)/self.player.price_last)*100


