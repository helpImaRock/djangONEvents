from django.contrib import admin

# Register your models here.
from apps.accounts.models import User, SignUpForm


class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
