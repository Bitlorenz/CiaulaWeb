from django.contrib import admin
from profiles.models import UserProfileModel


class UserProfileModelAdmin(admin.ModelAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    list_display = ('first_name', 'last_name', 'telefono', 'email', 'is_admin')
    list_filter = ('is_admin', 'first_name', 'last_name', 'email')
    search_fields = ('first_name__contains', 'last_name__contains', 'email__contains', 'telefono__contains')
    # fieldsets = ((None, {'fields': ('email', 'password')}), ('Permissions', {'fields': ('is_admin',)}),)
    exclude = ('last_login', 'groups', 'is_active', 'date_joined', 'user_permissions', 'is_superuser')
    # add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password'), }),)


admin.site.register(UserProfileModel, UserProfileModelAdmin)
