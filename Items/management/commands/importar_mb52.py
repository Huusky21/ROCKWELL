from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from Items.models import Accesorio, SOItem


class Command(BaseCommand):
    help = 'Importa accesorios y SO Items desde el archivo Excel mb52.'

    def add_arguments(self, parser):
        parser.add_argument(
            'ruta',
            nargs='?',
            default='mb52 power apps.xlsx',
            help='Ruta al archivo .xlsx (por defecto: "mb52 power apps.xlsx" en la raíz del proyecto).',
        )

    def handle(self, *args, **opts):
        try:
            import openpyxl
        except ImportError as exc:
            raise CommandError('Falta openpyxl. Instala con: pip install openpyxl') from exc

        ruta = Path(opts['ruta'])
        if not ruta.is_absolute():
            ruta = Path.cwd() / ruta
        if not ruta.exists():
            raise CommandError(f'No se encontró el archivo: {ruta}')

        wb = openpyxl.load_workbook(ruta, data_only=True)
        ws = wb.active

        nuevos_acc = 0
        nuevos_so = 0
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                continue
            accesorio_code = (row[0] or '').strip() if isinstance(row[0], str) else (str(row[0]).strip() if row[0] is not None else '')
            material = (row[1] or '').strip() if isinstance(row[1], str) else (str(row[1]).strip() if row[1] is not None else '')
            so_item = (row[2] or '').strip() if isinstance(row[2], str) else (str(row[2]).strip() if row[2] is not None else '')

            if accesorio_code:
                _, created = Accesorio.objects.get_or_create(codigo=accesorio_code)
                if created:
                    nuevos_acc += 1

            if so_item:
                obj, created = SOItem.objects.get_or_create(
                    so_item=so_item,
                    defaults={'material': material},
                )
                if created:
                    nuevos_so += 1
                elif material and obj.material != material:
                    obj.material = material
                    obj.save(update_fields=['material'])

        self.stdout.write(self.style.SUCCESS(
            f'Importación lista: {nuevos_acc} accesorios nuevos, {nuevos_so} SO Items nuevos.'
        ))
