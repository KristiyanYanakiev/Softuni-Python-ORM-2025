from django.contrib import admin

from main_app.models import House, Dragon, Quest


class OrderingAndReadOnlyFieldsAdmin(admin.ModelAdmin):
    ordering = ['-wins']
    readonly_fields = ['modified_at']

# Register your models here.
@admin.register(House)
class HouseAdmin(OrderingAndReadOnlyFieldsAdmin):
    list_display = ['name', 'wins', 'is_ruling']
    list_filter = ['is_ruling']
    search_fields = ['name', 'motto']


@admin.register(Dragon)
class DragonAdmin(OrderingAndReadOnlyFieldsAdmin):
    list_display = ['name', 'power', 'wins',  'breath', 'is_healthy']
    list_filter = ['is_healthy', 'breath']
    search_fields = ['name', 'breath']

@admin.register(Quest)
class QuestAdmin(OrderingAndReadOnlyFieldsAdmin):
    list_display = ['name', 'code', 'reward', 'start_time']
    list_filter = ['start_time','host__name']
    search_fields = ['host__name']
    ordering = ['start_time']
