from django.urls import path

from . import views

urlpatterns = [
    path('', views.registros_listado, name='registros_listado'),
    path('captura/', views.capturar, name='capturar'),
    path('exportar-excel/', views.export_excel, name='export_excel'),
    path('registro/<int:pk>/', views.registro_detalle, name='registro_detalle'),
    path('registro/<int:pk>/editar/', views.editar_registro, name='editar_registro'),
    path('registro/<int:pk>/eliminar/', views.registro_eliminar, name='registro_eliminar'),
    path('huacales/', views.huacales_inventario, name='huacales_inventario'),
    path('huacales/nuevo/', views.huacal_crear, name='huacal_crear'),
    path('huacales/<int:pk>/', views.huacal_detalle, name='huacal_detalle'),
    path('huacales/<int:pk>/editar/', views.huacal_editar, name='huacal_editar'),
    path('huacales/<int:pk>/eliminar/', views.huacal_eliminar, name='huacal_eliminar'),
    path('huacales/alertas/', views.huacales_alertas, name='huacales_alertas'),
]
