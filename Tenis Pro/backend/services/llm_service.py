from typing import cast
from openai import OpenAI
import os
from backend.models.order import Order

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_notification(order: Order) -> str:
    """
    Generates a notification email for an order.
    
    order: dict with keys -> id, product_type, product_name, amount, order_state
    """

    # Base context
    base_prompt = f"""
    You are an assistant that generates customer notifications for the sports distributor "Tenis Pro".
    The order details are:
    - Order ID: {order.id}
    - Product Type: {order.product_type}
    - Product Name: {order.product_name}
    - Amount: {order.amount}
    - Current Status: {order.order_state}
    """

    style = """
        Format the notification as an EMAIL with the following structure:
        - Subject line
        - Greeting
        - Order details in a clear list
        - Polite closing
        Example:
        Subject: Update on your Tenis Pro order #123 📦
        Hi Player!
        Your order has been updated:
        • Product: Professional Racket
        • Amount: 1
        • Status: DESPACHADO ✅
        Thank you for trusting Tenis Pro! 🎾
    """

    final_prompt = base_prompt + style

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate notifications for Tenis Pro customers."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.3
    )

    notification_text = cast(str, response.choices[0].message.content)
    
    return notification_text
