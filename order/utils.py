from django.core.mail import send_mail
from .models import Order


def send_successful_payment_message(email: str, order: Order):
	message = f"""
Заказ успешно оплачен

детали заказа:
Цена: {order.total_price}
Продукты:
"""
	for item in order.items.all():
		message += f"{item.product.title} ({item.quantity})\n"

	send_mail(
		subject="Успешный платеж",
		message=message,
		from_email="a@gmail.com",
		recipient_list=[email]
	)


def send_error_payment_message(email: str, order: Order):
	message = f"""
Заказ не был оплачен

детали заказа:
Цена: {order.total_price}
Продукты:
"""
	for item in order.items.all():
		message += f"{item.product.title} ({item.quantity})\n"

	send_mail(
		subject="Ошибка оплаты",
		message=message,
		from_email="a@gmail.com",
		recipient_list=[email]
	)