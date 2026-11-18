from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import uuid

class Product(models.Model):
    """Product model for e-commerce"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_price = models.DecimalField(max_digits=10, decimal_places=2)  # Lowest acceptable price
    discount_percentage = models.IntegerField(default=0)  # Current max discount allowed
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class NegotiationSession(models.Model):
    """Stores chat sessions and negotiation history"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Price tracking
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    offered_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_agreed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Session {self.session_id} - {self.product.name}"

    class Meta:
        ordering = ['-created_at']


class ChatMessage(models.Model):
    """Stores individual chat messages"""
    MESSAGE_TYPES = [
        ('user_text', 'User Text'),
        ('user_voice', 'User Voice'),
        ('bot_text', 'Bot Text'),
        ('bot_voice', 'Bot Voice'),
    ]

    session = models.ForeignKey(NegotiationSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField()  # For text messages
    audio_file = models.FileField(upload_to='chat_audio/', null=True, blank=True)  # For voice messages
    
    # Price offer information
    offered_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bot_response = models.TextField(null=True, blank=True)  # Bot's decision and reasoning
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_message_type_display()} - {self.session.session_id}"

    class Meta:
        ordering = ['created_at']


class PriceOffer(models.Model):
    """Tracks individual price offers"""
    OFFER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('counter', 'Counter Offer'),
    ]

    session = models.ForeignKey(NegotiationSession, on_delete=models.CASCADE, related_name='offers')
    offered_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=OFFER_STATUS_CHOICES, default='pending')
    
    # Bot decision reasoning
    reason = models.TextField()  # Why it was accepted/rejected
    counter_offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return f"Offer: ₹{self.offered_price} - {self.status}"

    class Meta:
        ordering = ['-created_at']


class Cart(models.Model):
    """Shopping cart with negotiated prices"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart - {self.user.username}"

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    """Individual items in cart with negotiated price"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    negotiation_session = models.ForeignKey(NegotiationSession, on_delete=models.SET_NULL, null=True, blank=True)
    
    quantity = models.IntegerField(default=1)
    negotiated_price = models.DecimalField(max_digits=10, decimal_places=2)  # Agreed price from negotiation
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    added_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.negotiated_price * self.quantity

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s cart"


class Order(models.Model):
    """Order created at checkout, stores billing and invoice media"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    final_total = models.DecimalField(max_digits=10, decimal_places=2)

    # Billing info snapshot
    billing_full_name = models.CharField(max_length=255, blank=True, null=True)
    billing_email = models.EmailField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_state = models.CharField(max_length=100, blank=True, null=True)
    billing_zip = models.CharField(max_length=20, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    invoice_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    negotiated_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.negotiated_price * self.quantity

    def __str__(self):
        return f"{self.product.name} x{self.quantity} for Order #{self.order.id}"

class AttendanceSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attendance Session {self.id}"

class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    attended_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session', 'date')
