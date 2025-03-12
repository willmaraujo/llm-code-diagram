# payment.py

class PaymentProcessor:
    def process_payment(self, amount):
        """Process payment if the amount is valid."""
        if amount <= 0:
            raise ValueError("Invalid amount")
        print(f"Processed payment of ${amount}")
        return True
