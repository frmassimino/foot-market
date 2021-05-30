from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .forms import BidModelForm, AskModelForm
from .models import Bid, Ask, Trade
from player.models import Player
from user.models import Portfolio

from django.contrib import messages 

# Create your views here.

def try_bid_operation(bid):
    queryset_ask = Ask.objects.filter(player=bid.player, status='Set').order_by('value','date_created')
    if len(queryset_ask) > 0:
        queryset_ask = queryset_ask[0:1]
        ask = queryset_ask[0]
        if bid.value >= ask.value:
            bid.owner.set_funds_variation(bid.value-ask.value)
            ask.owner.set_funds_variation(ask.value)
            bid_portfolio = Portfolio.objects.filter(user=bid.owner, player=bid.player)
            print(bid_portfolio.count)
            if not(bid_portfolio):
                bid_portfolio = Portfolio()
                bid_portfolio.player = bid.player
                bid_portfolio.count = 1
                bid_portfolio.compromised = 0
                bid_portfolio.user = bid.owner
                bid_portfolio.save()
            else:
                bid_portfolio = Portfolio.objects.get(user=bid.owner, player=bid.player)
                bid_portfolio.add_count()
            bid.bid_set_value(ask.value)
            bid.bid_close()
            ask_portfolio = Portfolio.objects.get(user=ask.owner, player=bid.player)
            ask_portfolio.sub_compromised()
            ask_portfolio.sub_count()
            bid.player.set_price_last(bid.player.get_price_actual()) 
            bid.player.set_price_actual(bid.value_actual)
            ask.ask_close()
            bid.save()
            ask.save()
        else:
            bid.owner.set_funds_variation(-bid.value)
    return bid

def try_ask_operation(ask):
    ask_portfolio = Portfolio.objects.filter(user=ask.owner, player=ask.player)
    ask_portfolio = ask_portfolio[0]
    ask_portfolio.add_compromised()
    queryset_bid = Bid.objects.filter(player=ask.player, status='Set').order_by('-value','date_created')
    if len(queryset_bid) > 0:
        queryset_bid = queryset_bid[0:1]
        bid = queryset_bid[0]
        if ask.value <= bid.value:
            ask.owner.set_funds_variation(bid.value)      
            ask_portfolio.sub_compromised()
            ask_portfolio.sub_count()
            bid_portfolio = Portfolio.objects.filter(user=bid.owner, player=bid.player)
            if not(bid_portfolio):
                bid_portfolio = Portfolio()
                bid_portfolio.player = bid.player
                bid_portfolio.count = 1
                bid_portfolio.compromised = 0
                bid_portfolio.user = bid.owner
                bid_portfolio.save()
            else:
                bid_portfolio = Portfolio.objects.get(user=bid.owner, player=bid.player)
                bid_portfolio.add_count()
            ask.player.set_price_last(ask.player.get_price_actual()) 
            ask.player.set_price_actual(ask.value)
            ask.ask_set_value(bid.value)
            ask.ask_close()
            bid.bid_close()
            bid.save()
            ask.save()
    return ask

def get_player(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj

class TradeStatus(View):
    template_name = "trades_status.html"

    def get_bid_queryset(self):
        queryset = Bid.objects.filter(trade__player__id = self.kwargs.get('id')).order_by('value')
        print(queryset)
        return reversed(list(queryset))

    def get_ask_queryset(self):
        queryset = Ask.objects.filter(trade__player__id = self.kwargs.get('id')).order_by('value')
        print(queryset)
        return queryset

    def get(self, request, *args, **kwargs):
        context = {
            'bid_object_list': self.get_bid_queryset(),
            'ask_object_list': self.get_ask_queryset(),
        }
        return render(request, self.template_name, context)

class TradeOverview(View):
    model = Player
    template_name = "trade_overview.html"

    def get_bid_queryset(self):
        queryset = Bid.objects.filter(player__id = self.kwargs.get('id')).order_by('-value','date_created')
        print(queryset)
        return queryset

    def get_ask_queryset(self):
        queryset = Ask.objects.filter(player__id = self.kwargs.get('id')).order_by('value','date_created')
        print(queryset)
        return queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': get_player(self),
                    'bid_object_list': self.get_bid_queryset(),
                    'ask_object_list': self.get_ask_queryset(),
                    }
        return render(request, self.template_name, context)


class BidObjectMixin(object):
    model = Bid

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj

class BidListView(View):
    template_name = "bid_list.html"

    def get_queryset(self):
        queryset = Bid.objects.all().order_by('value')
        return reversed(list(queryset))

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset()}
        return render(request, self.template_name, context)

class BidCreateView(View):
    template_name = "bid_create.html" #DetailView

    def get(self, request, *args, **kwargs):
        # GET method
        form = BidModelForm()
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # POST method
        form = BidModelForm(request.POST)
        if form.is_valid():
            preForm = form.save(commit=False)
            preForm.owner = request.user
            if preForm.value > 0:
                if preForm.owner.get_funds() >= preForm.value:
                    #preForm.trade = Trade.objects.get(player__id=self.kwargs.get('id'))
                    preForm.player = Player.objects.get(id=self.kwargs.get('id'))
                    preForm.status = 'Set'
                    preForm.value_last = preForm.value
                    preForm.value_actual = preForm.value
                    #preForm = try_operation(preForm, 'bid')
                    preForm = try_bid_operation(preForm)
                    form = preForm
                    print(form.date_created)
                    form.save()
                    form = BidModelForm()
                    messages.success(request,"Bid setted successfully!")
                else:
                    messages.error(request,"You don't have enough money.")
            else:
                messages.error(request,"Value can't be 0")
        context = {"form": form}
        return render(request, self.template_name, context)

class BidDeleteView(BidObjectMixin, View):
    template_name = "bid_delete.html" #DetailView

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None and obj.status != 'Done':
            obj.bid_cancel()
            obj.owner.set_funds_variation(obj.value)
            context['object'] = None
            return redirect('/trade/trades_status/')
        else:
            messages.error(request,'Cannot delete a completed operation')
        return render(request, self.template_name, context)

class BidUpdateView(BidObjectMixin, View):
    template_name = "bid_update.html" #DetailView

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = BidModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = BidModelForm(request.POST, instance=obj)
            if form.is_valid() and obj.status != 'Done':
                preForm = form.save(commit=False)
                funds = preForm.owner.get_funds()
                if (funds+preForm.value_actual) >= preForm.value:
                    preForm.owner.set_funds_variation(-(preForm.value-preForm.value_actual))
                    preForm.value_last = preForm.value_actual
                    preForm.value_actual = preForm.value
                    preForm = try_bid_operation(preForm)
                    form = preForm
                    form.save()
                    form = BidModelForm()
                else:
                    messages.error(request,"You don't have enough money to complete the operation.")
            else:
                messages.error(request,'Cannot edit a completed operation.')
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

class AskObjectMixin(object):
    model = Ask

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj

class AskListView(View):
    template_name = "ask_list.html"

    def get_queryset(self):
        queryset = Ask.objects.all().order_by('value')
        return queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset()}
        return render(request, self.template_name, context)

class AskCreateView(View):
    template_name = "ask_create.html" #DetailView

    def get(self, request, *args, **kwargs):
        # GET method
        form = AskModelForm()
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # POST method
        form = AskModelForm(request.POST)
        if form.is_valid():
            preForm = form.save(commit=False)
            preForm.owner = request.user
            #preForm.trade = Trade.objects.get(player__id=self.kwargs.get('id'))
            preForm.player = Player.objects.get(id=self.kwargs.get('id'))
            preForm.status = 'Set'
            ask_portfolio = Portfolio.objects.filter(user=preForm.owner, player=preForm.player)
            if ask_portfolio and ask_portfolio[0].check_count():
                preForm = try_ask_operation(preForm)
                form = preForm
                form.save()
            else:
                messages.error(request,'You dont have enough assets.')
            form = AskModelForm()
        context = {"form": form}
        print(context)
        return render(request, self.template_name, context)

class AskDeleteView(AskObjectMixin, View):
    template_name = "ask_delete.html" #DetailView

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None and obj.status != 'Done':
            obj.ask_cancel()
            context['object'] = None
            return redirect('/user/user_overview/')
        else:
            messages.error(request,'Cannot delete a completed operation')
        return render(request, self.template_name, context)

class AskUpdateView(AskObjectMixin, View):
    template_name = "ask_update.html" #DetailView

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AskModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AskModelForm(request.POST, instance=obj)
            if form.is_valid() and obj.status != 'Done':
                preForm = form.save(commit=False)
                preForm.owner = request.user
                preForm.status = 'Set'
                preForm = try_ask_operation(preForm)
                form = preForm
                form.save()
            else:
                messages.error(request,'Cannot edit a completed operation.')
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)