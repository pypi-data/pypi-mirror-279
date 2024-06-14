from django.db.models.signals import pre_save
from django.dispatch import receiver
from artd_order.models import Order


@receiver(pre_save, sender=Order)
def set_increment_id(sender, instance, **kwargs):
    # Verifica si es una nueva instancia (no tiene un ID asignado)
    if instance.pk is None:
        # Obtiene el último increment_id para el partner y lo incrementa en uno
        last_order = (
            Order.objects.filter(partner=instance.partner)
            .order_by("-increment_id")
            .first()
        )
        if last_order:
            instance.increment_id = last_order.increment_id + 1
        else:
            # Si es el primer Order para el Partner, establece el increment_id en 1
            instance.increment_id = 1
