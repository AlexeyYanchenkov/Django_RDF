import stripe
from django.conf import settings
from stripe.error import StripeError

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(name):
    try:
        product = stripe.Product.create(name=name)
        return product.id
    except StripeError as e:
        print(f"Ошибка при создании продукта: {e}")
        raise Exception("Не удалось создать продукт Stripe")

def create_stripe_price(product_id, amount):
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=int(amount * 100),  # рубли → копейки
            currency='rub'
        )
        return price.id
    except StripeError as e:
        print(f"Ошибка при создании цены: {e}")
        raise Exception("Не удалось создать цену в Stripe")

def create_stripe_session(price_id, success_url, cancel_url):
    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price': price_id,
                'quantity': 1
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url
        )
        return session.url
    except StripeError as e:
        print(f"Ошибка при создании сессии оплаты: {e}")
        raise Exception("Не удалось создать платёжную сессию в Stripe")