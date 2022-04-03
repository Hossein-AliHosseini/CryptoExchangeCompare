from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Person, ActivateUserToken
from .forms import CustomUserCreationForm, CustomUserChangeForm


class PersonInline(admin.StackedInline):
    model = Person


class CustomUserAdmin(UserAdmin):
    inlines = [PersonInline, ]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(ActivateUserToken)
admin.site.register(Person)
