from django.core.mail import send_mail
from celery import shared_task
from .models import Product
from datetime import date, timedelta
from account.models import User


@shared_task
def send_new_products():
    day = date.today() - timedelta(days=1)
    products = Product.objects.filter(created_at__gte=day)
    message = f"Новые продукты"
    for product in products:
        message += f"\n{product.title}  ${product.price}"

    send_mail(
        subject="Новинки, часы casio за 20$",
        message=message,
        from_email="aminuwko@gmail.com",
        recipient_list=[u.email for u in User.objects.all()]
    )