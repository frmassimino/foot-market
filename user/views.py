from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.admin.views.decorators import staff_member_required
from django.views import View

from .models import CustomUser, Portfolio
from ipo.models import Bidder
from trade.models import Bid, Ask 
from .forms import UserModelForm
#from .forms import UserModelForm
#---------------------------------------
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
#---------------------------------------
from .forms import UserCreateForm 
# Create your views here.

user_initial_funds = 100000000

class CustomUserObjectMixin(object):
    model = CustomUser

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj

#@staff_member_required
#@login_required
class UserOverviewView(View):
    template_name = "user_overview.html"

    def get_portfolio_queryset(self, request):
        queryset = Portfolio.objects.filter(user__id = request.user.id)
        return queryset

    def get_bidder_queryset(self, request):
        queryset = Bidder.objects.filter(bidder__id = request.user.id).order_by('-date_created')
        return queryset

    def get_bid_queryset(self, request):
        queryset_bid = Bid.objects.filter(owner__id = request.user.id).order_by('-date_created')
        return queryset_bid
        
    def get_ask_queryset(self, request):
        queryset_ask = Ask.objects.filter(owner__id = request.user.id).order_by('-date_created')
        return queryset_ask

    def get(self, request, *args, **kwargs):
        context = {'portfolio': self.get_portfolio_queryset(request),
                    'bidder':self.get_bidder_queryset(request),
                    'bid':self.get_bid_queryset(request),
                    'ask':self.get_ask_queryset(request)}
        return render(request, self.template_name, context)

class UserHistoryView(View):
    template_name = "user_history.html"

    def get_bidder_queryset(self, request):
        queryset = Bidder.objects.filter(bidder__id = request.user.id).exclude(status='Set')
        return queryset

    def get_bid_queryset(self, request):
        queryset_bid = Bid.objects.filter(owner__id = request.user.id).exclude(status='Set')
        return queryset_bid
        
    def get_ask_queryset(self, request):
        queryset_ask = Ask.objects.filter(owner__id = request.user.id).exclude(status='Set')
        return queryset_ask

    def get(self, request, *args, **kwargs):
        context = {'bidder':self.get_bidder_queryset(request),
                    'bid':self.get_bid_queryset(request),
                    'ask':self.get_ask_queryset(request)}
        return render(request, self.template_name, context)

#class UserRegisterView(View):
#    template_name = "user_register.html" #DetailView

#    def get(self, request, *args, **kwargs):
#        # GET method
#        form = UserModelForm()
#        context = {"form": form}
#        return render(request, self.template_name, context)
#    
#    def post(self, request, *args, **kwargs):
#        # POST method
#        form = UserModelForm(request.POST)
#        if form.is_valid():
#            form.save()
#            form = UserModelForm()
#        context = {"form": form}
#        return render(request, self.template_name, context)

class UserRegisterView(View):
    template_name = "user_register.html" #DetailView
        
    def get(self, request, *args, **kwargs):
        # GET method
        form = UserCreateForm()
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # POST method
        form = UserCreateForm(request.POST)
        if form.is_valid():
            preForm = form.save(commit=False)
            preForm.funds = user_initial_funds
            print(preForm.funds)
            form = preForm
            form.save()
            auth_login(self.request, form.get_user())
            return redirect('/home/')
        else:
            form = UserCreateForm()
        context = {"form": form}
        return render(request, self.template_name, context)

class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/home/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'user_login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        #redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        redirect_to = '/user/user_overview/'
        #if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            #redirect_to = self.success_url
        return redirect_to

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/home/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)