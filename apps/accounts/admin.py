from django.contrib import admin

# Register your models here.
from apps.accounts.models import User,SignUpForm


class UserAdmin(admin.ModelAdmin):
    pass
   #form = SignUpForm
   #def save_model(self, request, obj, form, change):
   #    obj.user = request.user
   #    obj.user.email="admin@none.com"
   #    super().save_model(request, obj, form, change)

admin.site.register(User,UserAdmin)