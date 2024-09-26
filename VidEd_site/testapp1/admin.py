from django.contrib import admin

from testapp1.models import *
# Register your models here.

# admin.site.register(User)
# admin.site.register(Message)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'second_name', 'email', 'telegram_id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'creator', 'worker', 'deadline')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'date', 'address')

@admin.register(UrlsOrders)
class UrlsOrdersAdmin(admin.ModelAdmin):
    list_display = ('order', 'url_isCloud', 'url')

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ("groupname", "privilege_level")

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ("user", "sk_prempro", "sk_aftereffects")

@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'description', 'callback')



