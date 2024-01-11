def process_customer_order(order_data):
    # Step 1: Validate input order data
    if not order_data:
        raise ValueError("Invalid order data")

    # Step 2: Extract customer information
    customer_info = order_data.get('customer_info', {})
    if not customer_info:
        raise ValueError("Customer information missing in order data")

    customer_name = customer_info.get('name', '')
    customer_email = customer_info.get('email', '')
    customer_address = customer_info.get('address', '')

    # Step 3: Extract order details
    order_details = order_data.get('order_details', [])
    if not order_details:
        raise ValueError("Order details missing in order data")

    total_amount = 0
    for item in order_details:
        # Calculate item subtotal
        item_price = item.get('price', 0)
        item_quantity = item.get('quantity', 0)
        item_subtotal = item_price * item_quantity

        # Add to the total amount
        total_amount += item_subtotal

    # Step 4: Apply discounts
    if total_amount > 100:
        total_amount *= 0.9  # 10% discount for orders over $100

    # Step 5: Generate order summary
    order_summary = f"Customer: {customer_name}, Email: {customer_email}, Address: {customer_address}\n"
    order_summary += "Order Details:\n"
    for item in order_details:
        order_summary += f"- {item.get('name', '')}: ${item.get('price', 0)} x {item.get('quantity', 0)}\n"
    order_summary += f"Total Amount: ${total_amount}"

    # Step 6: Send order confirmation email
    send_order_confirmation_email(customer_email, order_summary)
    
    # Step 7: Print success message
    print("Order processing completed successfully")

