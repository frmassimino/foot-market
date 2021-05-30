from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .models import Ipo, Bidder
from .forms import IpoModelForm

from django.contrib import messages
# Create your views here.

class IpoObjectMixin(object):
    model = Bidder

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj

class IpoListView(View):
    template_name = "ipo_list.html"

    def get_queryset(self):
        queryset = Ipo.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset()}
        return render(request, self.template_name, context)

class IpoBidCreateView(View):
    template_name = "ipo_bid.html" #DetailView

    def get(self, request, *args, **kwargs):
        # GET method
        form = IpoModelForm()
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # POST method
        form = IpoModelForm(request.POST)
        if form.is_valid():
            preForm = form.save(commit=False)
            preForm.bidder = request.user
            preForm.ipo = Ipo.objects.get(id=self.kwargs.get('id'))
            preForm.status = 'Set'
            if preForm.check_funds(request.user) and preForm.ipo.get_ipo_status() != 'Closed':
                preForm.bidder.set_funds_variation(-(preForm.value))
                preForm.value_last = preForm.value
                preForm.value_actual = preForm.value
                form = preForm
                form.save()
                form = IpoModelForm()
            else:
                messages.error(request,'IPO already closed.')
        context = {"form": form}
        return render(request, self.template_name, context)

class IpoBidDeleteView(IpoObjectMixin, View):
    template_name = "ipo_delete.html" #DetailView

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
            obj.bidder.set_funds_variation(obj.value)
            obj.bidder_cancel()
            context['object'] = None
            return redirect('/user/user_overview/')
        else:
            messages.error(request,'Cannot delete a completed operation')
        return render(request, self.template_name, context)

class IpoBidUpdateView(IpoObjectMixin, View):
    template_name = "ipo_update.html" #DetailView

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IpoModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        print(obj)
        if obj is not None:
            form = IpoModelForm(request.POST, instance=obj)
            if form.is_valid() and obj.status != 'Done':
                preForm = form.save(commit=False)
                funds = preForm.bidder.get_funds()
                if (funds+preForm.value_actual) >= preForm.value:
                    preForm.bidder.set_funds_variation(-(preForm.value-preForm.value_actual))
                    preForm.value_last = preForm.value_actual
                    preForm.value_actual = preForm.value
                    form = preForm
                    form.save()
                    form = IpoModelForm()
                else:
                    messages.error(request,"You don't have enough funds.")
            else:
                messages.error(request,'Cannot edit a completed operation.')
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

class IpoCloseView(View):
    template_name = "ipo_close.html"

    def get_ipo(self):
        ipo = Ipo.objects.get(id=self.kwargs.get('id'))
        return ipo
    
    def get_bidders(self):
        winners = 0
        ipo = self.get_ipo()
        queryset_bidders = Bidder.objects.filter(ipo=ipo)
        queryset_bidders_winner = list(queryset_bidders.order_by('-value'))[0:ipo.get_ipo_count()]
        for bidder in queryset_bidders:
            bidder.bidder_close()
            bidder.save()
        for bidder in queryset_bidders_winner:
            bidder.bidder_close_winner()
            bidder.save()
            winners = winners + 1
        ipo.player.set_ipo_last(queryset_bidders_winner[0].value)
        ipo.ipo_close(winners)
        ipo.save()
        return 'Done'
    
    def get(self, request, *args, **kwargs):
        context = {'result' : self.get_bidders()}
        return render(request, self.template_name, context)

