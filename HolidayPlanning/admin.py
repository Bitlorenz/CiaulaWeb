from django.contrib import admin

from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username" field
    fields = ["username"]


#admin.site.unregister(User)
#admin.site.unregister(Group)

# Register your models here.

#admin.site.register(User, UserAdmin)