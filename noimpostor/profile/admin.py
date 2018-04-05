from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUser
from django.contrib import admin
from .models import DefaultPrivacy

class UserDefaultPrivacyInline(admin.StackedInline):
    model = DefaultPrivacy
    can_delete = False
    verbose_name = 'privacy setting'
    verbose_name_plural = 'user privacy settings'


class UserAdmin(BaseUser):
    inlines = [UserDefaultPrivacyInline]


admin.site.unregister(User)
admin.register(DefaultPrivacy)
admin.site.register(User, UserAdmin)
