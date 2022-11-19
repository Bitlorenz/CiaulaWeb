from django.contrib import admin
from .models import Attrazione
from django.contrib.auth.models import User, Group


class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username" field
    fields = ["username"]


admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
admin.site.register(Attrazione)
admin.site.register(User, UserAdmin)