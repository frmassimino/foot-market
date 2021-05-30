from django.db import models

# Create your models here.

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=True, blank=False)

    def __str__(self):
        return(self.name)

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=False, blank=False)
    surname = models.CharField(max_length=120,null=False, blank=False)
    age = models.CharField(max_length=120, null=False, blank=False)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=False)
    price_actual = models.IntegerField(default=1)
    price_last = models.IntegerField(default=1)
    price_theorical = models.IntegerField(default=1)
    ipo_last = models.IntegerField(default=0)
    pool = models.IntegerField(default=1)
    rating = models.CharField(max_length=120, null=False, blank=False, default = '100%')

    def __str__(self):
        return ('{0} {1}'.format(self.name, self.surname))

    def get_name(self):
        return(f'{self.name} {self.surname}')

    def get_value_percentege(self):
        return ((self.price_actual-self.price_last)/self.price_last)*100

    def expand_pool(self, amount):
        self.pool = self.pool + amount

    def set_price_last(self, price):
        self.price_last = price
        self.save()

    def get_price_last(self):
        return self.price_last

    def set_price_actual(self, price):
        self.price_last = price
        self.save()

    def get_price_actual(self):
        return self.price_actual
    
    def set_ipo_last(self, price):
        self.ipo_last = price
        self.save()