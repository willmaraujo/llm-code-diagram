# payment.py

class PaymentProcessor:
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")
        print(f"Processed payment of ${amount}")
        return True
