from django.db import migrations


PALLETS = [
    ('PN-48336', 'Tarima 5CLs', '46x36"', 30),
    ('PN-68388', 'Celdas, UPS', '48x48"', 90),
    ('PN-126921', 'Tarima para 1 seccion es igual qu', '43x36"', 50),
    ('PN-126923', 'MCC', '63x36"', 25),
    ('PN-126922', 'MCC', '43x36"', 21),
    ('PN-126919', 'MCC', '43x36"', 15),
    ('40121-982-01', 'MCC de exportacion', '43x36"', 10),
    ('PN-219674', 'SSB', '48x72"', 8),
    ('PN-494419', 'AMAT, Tere', '48x72"', 20),
    ('PN-70950', 'Celdas', '', 20),
    ('PN-68389', 'SSB', '96x48"', 15),
    ('PN-66376', 'Se usa en FAB', '43x36"', 8),
    ('40121-983-01', 'MCC de exportacion', '43x36"', 3),
    ('PN-146624', 'Celdas', '43x36"', 4),
    ('PN-494423', 'AMAT, Tere', '', 4),
    ('PN-65651', 'SSB', '144x48"', 1),
    ('PN-641910', 'SSB', '48x48"', 5),
]


CRATES = [
    ('PN-E081123', '30 de cada uno al final de mes', '', 9),
    ('PN-E081124', '30 de cada uno al final de mes', '', 24),
    ('PN-E084715', '30 de cada uno al final de mes', 'UNITS', 2),
    ('PN-525689', '30 de cada uno al final de mes', '48x48"', 20),
    ('PN-525692', '30 de cada uno al final de mes', '48x72"', 10),
    ('PN-525694', '30 de cada uno al final de mes', '48x96"', 1),
    ('PN-73592', '', '', 0),
    ('PN-748464', 'porterias onmachine', '', 40),
    ('PN-115654', '', '', 10),
]


def cargar_huacales(apps, schema_editor):
    Huacal = apps.get_model('Items', 'Huacal')
    for pn, descripcion, medidas, consumo in PALLETS:
        Huacal.objects.get_or_create(
            pn=pn,
            defaults={
                'descripcion': descripcion,
                'medidas': medidas,
                'consumo_semanal': consumo,
                'tipo': 'pallet',
            },
        )
    for pn, descripcion, medidas, consumo in CRATES:
        Huacal.objects.get_or_create(
            pn=pn,
            defaults={
                'descripcion': descripcion,
                'medidas': medidas,
                'consumo_semanal': consumo,
                'tipo': 'crate',
            },
        )


def borrar_huacales(apps, schema_editor):
    Huacal = apps.get_model('Items', 'Huacal')
    pns = [pn for pn, *_ in PALLETS] + [pn for pn, *_ in CRATES]
    Huacal.objects.filter(pn__in=pns).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0007_conteohuacal_huacal_remove_movimientohuacal_usuario_and_more'),
    ]

    operations = [
        migrations.RunPython(cargar_huacales, borrar_huacales),
    ]
