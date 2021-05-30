from django.shortcuts import render
from django.views import View

from .models import Player
# Create your views here.

class PlayersList(View):
    template_name = "players_list.html"

    def get_queryset(self):
        return Player.objects.all()

    def get(self, request, *args, **kwargs):
        context = {
            'object_list': self.get_queryset(),
        }
        return render(request, self.template_name, context)