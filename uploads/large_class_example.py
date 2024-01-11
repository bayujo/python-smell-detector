class Order:
    def __init__(self, customer, items):
        self.customer = customer
        self.items = items
        self.total_price = 0

    def calculate_total_price(self):
        for item in self.items:
            self.total_price += item.price

    def process_order(self):
        self.calculate_total_price()
        self.apply_discount()
        self.calculate_tax()
        self.generate_invoice()
        self.send_confirmation_email()

    def apply_discount(self):
        # Placeholder code for applying discounts
        discount_rate = 0.1  # 10% discount for illustration purposes
        self.total_price -= self.total_price * discount_rate

    def calculate_tax(self):
        # Placeholder code for calculating tax
        tax_rate = 0.07  # 7% tax for illustration purposes
        self.total_price += self.total_price * tax_rate

    def generate_invoice(self):
        # Placeholder code for generating an invoice
        invoice_content = f"Invoice for {self.customer}: Total Price - ${self.total_price}"
        print(invoice_content)

    def send_confirmation_email(self):
        # Placeholder code for sending a confirmation email
        email_content = f"Thank you for your order, {self.customer}! Your order is confirmed."
        print(email_content)
    
    def calculate_total_price2(self):
        for item in self.items:
            self.total_price += item.price

    def process_order2(self):
        self.calculate_total_price()
        self.apply_discount()
        self.calculate_tax()
        self.generate_invoice()
        self.send_confirmation_email()

    def apply_discount2(self):
        # Placeholder code for applying discounts
        discount_rate = 0.1  # 10% discount for illustration purposes
        self.total_price -= self.total_price * discount_rate

    def calculate_tax2(self):
        # Placeholder code for calculating tax
        tax_rate = 0.07  # 7% tax for illustration purposes
        self.total_price += self.total_price * tax_rate

    def generate_invoice2(self):
        # Placeholder code for generating an invoice
        invoice_content = f"Invoice for {self.customer}: Total Price - ${self.total_price}"
        print(invoice_content)

    def send_confirmation_email2(self):
        # Placeholder code for sending a confirmation email
        email_content = f"Thank you for your order, {self.customer}! Your order is confirmed."
        print(email_content)
        
    def calculate_total_price3(self):
        for item in self.items:
            self.total_price += item.price

    def process_order3(self):
        self.calculate_total_price()
        self.apply_discount()
        self.calculate_tax()
        self.generate_invoice()
        self.send_confirmation_email()

    def apply_discount3(self):
        # Placeholder code for applying discounts
        discount_rate = 0.1  # 10% discount for illustration purposes
        self.total_price -= self.total_price * discount_rate

    def calculate_tax3(self):
        # Placeholder code for calculating tax
        tax_rate = 0.07  # 7% tax for illustration purposes
        self.total_price += self.total_price * tax_rate

    def generate_invoice3(self):
        # Placeholder code for generating an invoice
        invoice_content = f"Invoice for {self.customer}: Total Price - ${self.total_price}"
        print(invoice_content)

    def send_confirmation_email3(self):
        # Placeholder code for sending a confirmation email
        email_content = f"Thank you for your order, {self.customer}! Your order is confirmed."
        print(email_content)

    def calculate_total_price4(self):
        for item in self.items:
            self.total_price += item.price

    def process_order4(self):
        self.calculate_total_price()
        self.apply_discount()
        self.calculate_tax()
        self.generate_invoice()
        self.send_confirmation_email()

    def apply_discount4(self):
        # Placeholder code for applying discounts
        discount_rate = 0.1  # 10% discount for illustration purposes
        self.total_price -= self.total_price * discount_rate

    def calculate_tax4(self):
        # Placeholder code for calculating tax
        tax_rate = 0.07  # 7% tax for illustration purposes
        self.total_price += self.total_price * tax_rate

    def generate_invoice4(self):
        # Placeholder code for generating an invoice
        invoice_content = f"Invoice for {self.customer}: Total Price - ${self.total_price}"
        print(invoice_content)

    def send_confirmation_email4(self):
        # Placeholder code for sending a confirmation email
        email_content = f"Thank you for your order, {self.customer}! Your order is confirmed."
        print(email_content)