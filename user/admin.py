from django.contrib import admin
from django.contrib.auth import get_user_model
#from django.contrib.auth.admin import UserAdmin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreateForm, UserChangeForm
from .models import CustomUser, Portfolio

#admin.site.register(CustomUser, UserAdmin)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['username','email', 'funds']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Portfolio)