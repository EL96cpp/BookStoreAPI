from django.template.loader import render_to_string
from django.core.mail import send_mail
from bookstore import celery_app


@celery_app.task
def send_order_email(email_host_user: str, user_email: str, store_address: str, 
                     books: list[dict], total: int):
    html_message = render_to_string('orders/order_email.html', 
                                    {'title': "Вы успешно оформили заказ", 'store_address': store_address,
                                     'books': books, 'total': total})
    send_mail(
        "Оформление заказа",
        "Вы успешно оформили заказ",
        email_host_user,
        [user_email],
        html_message=html_message,
        fail_silently=False
    )