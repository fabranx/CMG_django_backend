from django.contrib import admin

# Register your models here.

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# from .models import Profile

from .forms import  CustomUserChangeForm, CustomUserCreationForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username','image',]  #cosa mostrare nella pagina admin/users
    fieldsets = UserAdmin.fieldsets + (  # fields aggiunti nella pagina di modifica degli users
        ('Profile Image', { 
            "fields": (
                'image',
            ),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (  # fields aggiunti nella pagina di aggiunta nuovo users
        (None, {
            'fields': ('email',),
        }),
        ('Profile Image', {
            'fields': ('image',),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Profile)


# SERVE PER PERMETTERE L'ELIMINAIZONE DEGLI USERS QUANDO SI USA LA BLACKLIST DEI TOKEN
# ALTRIMENTI NON SARÀ POSSIBILE ELIMINARE GLI USERS A CAUSA DI:  OUSTANDING TOKEN ERROR
from rest_framework_simplejwt import token_blacklist

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)