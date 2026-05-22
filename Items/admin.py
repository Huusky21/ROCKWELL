from django.contrib import admin

from .models import Accesorio, Registro, SOItem


@admin.register(Accesorio)
class AccesorioAdmin(admin.ModelAdmin):
    list_display = ('codigo',)
    search_fields = ('codigo',)


@admin.register(SOItem)
class SOItemAdmin(admin.ModelAdmin):
    list_display = ('so_item', 'material')
    search_fields = ('so_item', 'material')


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('so_item', 'accesorio', 'cantidad', 'creado')
    list_filter = ('accesorio',)
    search_fields = ('so_item__so_item', 'accesorio__codigo')
    autocomplete_fields = ('so_item', 'accesorio')
