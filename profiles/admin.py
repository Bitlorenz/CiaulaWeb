from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from profiles.models import UserProfileModel
from profiles.forms import UserCreationForm, UserChangeForm


class UserProfileModelAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    exclude = ('last_login', 'groups', 'is_active', 'date_joined', 'user_permissions')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(UserProfileModel, UserProfileModelAdmin)

#list_display = ('first_name', 'last_name', 'username', 'email', 'date_joined')
#list_filter = ('first_name', 'last_name', 'username')
#search_fields = ('first_name__contains', 'last_name__contains', 'username__contains')
#exclude = ('last_login', 'groups', 'is_active', 'date_joined', 'user_permissions')