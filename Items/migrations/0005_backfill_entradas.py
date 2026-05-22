from django.db import migrations


def crear_entradas_iniciales(apps, schema_editor):
    Registro = apps.get_model('Items', 'Registro')
    Entrada = apps.get_model('Items', 'Entrada')
    for registro in Registro.objects.all():
        entrada = Entrada.objects.create(
            registro=registro,
            cantidad=registro.cantidad,
            usuario=registro.usuario,
        )
        Entrada.objects.filter(pk=entrada.pk).update(creado=registro.creado)


def borrar_entradas_iniciales(apps, schema_editor):
    Entrada = apps.get_model('Items', 'Entrada')
    Entrada.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0004_entrada'),
    ]

    operations = [
        migrations.RunPython(crear_entradas_iniciales, borrar_entradas_iniciales),
    ]
