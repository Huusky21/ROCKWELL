from django.conf import settings
from django.db import models


class Accesorio(models.Model):
    codigo = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Accesorio'
        verbose_name_plural = 'Accesorios'
        ordering = ['codigo']

    def __str__(self):
        return self.codigo


class SOItem(models.Model):
    so_item = models.CharField(max_length=50, unique=True)
    material = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'SO Item'
        verbose_name_plural = 'SO Items'
        ordering = ['so_item']

    def __str__(self):
        if self.material:
            return f'{self.so_item} ({self.material})'
        return self.so_item


class Registro(models.Model):
    so_item = models.ForeignKey(SOItem, on_delete=models.PROTECT, related_name='registros')
    accesorio = models.ForeignKey(Accesorio, on_delete=models.PROTECT, related_name='registros', blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f'{self.so_item} x {self.cantidad}'


class Entrada(models.Model):
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE, related_name='entradas')
    cantidad = models.PositiveIntegerField()
    huacal = models.ForeignKey(
        'Huacal',
        on_delete=models.SET_NULL,
        related_name='entradas',
        blank=True,
        null=True,
    )
    accesorio = models.ForeignKey(
        Accesorio,
        on_delete=models.SET_NULL,
        related_name='entradas',
        blank=True,
        null=True,
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['-creado']

    def __str__(self):
        return f'{self.registro.so_item} +{self.cantidad} ({self.creado:%d/%m/%Y %H:%M})'


class Huacal(models.Model):
    PALLET = 'pallet'
    CRATE = 'crate'
    TIPO_CHOICES = [(PALLET, 'Pallets'), (CRATE, 'Crates')]

    pn = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)
    medidas = models.CharField(max_length=50, blank=True)
    consumo_semanal = models.PositiveIntegerField(default=0)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default=PALLET)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Huacal'
        verbose_name_plural = 'Huacales'
        ordering = ['tipo', 'pn']

    def __str__(self):
        return self.pn


class ConteoHuacal(models.Model):
    huacal = models.ForeignKey(Huacal, on_delete=models.CASCADE, related_name='conteos')
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conteo de huacal'
        verbose_name_plural = 'Conteos de huacal'
        ordering = ['-fecha']
        constraints = [
            models.UniqueConstraint(fields=['huacal', 'fecha'], name='conteo_huacal_fecha_unique'),
        ]

    def __str__(self):
        return f'{self.huacal.pn} {self.fecha:%d/%m/%Y} = {self.cantidad}'


class DestinatarioAlertaHuacal(models.Model):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Destinatario de alerta'
        verbose_name_plural = 'Destinatarios de alerta'
        ordering = ['email']

    def __str__(self):
        return f'{self.nombre} <{self.email}>' if self.nombre else self.email


class MensajeAlertaHuacal(models.Model):
    asunto = models.CharField(
        max_length=200,
        default='Alerta: inventario de huacales agotado',
    )
    cuerpo = models.TextField(
        default=(
            'El inventario de huacales ha llegado a 0.\n'
            'Es necesario reabastecer cuanto antes.\n'
        ),
    )

    class Meta:
        verbose_name = 'Mensaje de alerta'
        verbose_name_plural = 'Mensaje de alerta'

    def __str__(self):
        return self.asunto

    @classmethod
    def obtener(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
