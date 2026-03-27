from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = 'Populate database with sample products for testing'

    def handle(self, *args, **options):
        # Sample products data
        products_data = [
            {
                'name': 'Premium Laptop',
                'description': 'High-performance laptop with Intel i7, 16GB RAM, and 512GB SSD. Perfect for professionals and content creators.',
                'original_price': 1299.99,
                'minimum_price': 899.99,
                'discount_percentage': 30,
                'stock': 5
            },
            {
                'name': 'Smart Watch Pro',
                'description': 'Advanced smartwatch with heart rate monitor, GPS, and 7-day battery life. Water-resistant up to 50m.',
                'original_price': 399.99,
                'minimum_price': 249.99,
                'discount_percentage': 35,
                'stock': 12
            },
            {
                'name': 'Wireless Headphones',
                'description': 'Premium noise-cancelling headphones with 40-hour battery. Active noise cancellation and premium audio quality.',
                'original_price': 349.99,
                'minimum_price': 199.99,
                'discount_percentage': 40,
                'stock': 20
            },
            {
                'name': '4K Webcam',
                'description': '4K resolution webcam with auto-focus and built-in microphone. Perfect for streaming and video calls.',
                'original_price': 199.99,
                'minimum_price': 99.99,
                'discount_percentage': 45,
                'stock': 15
            },
            {
                'name': 'Mechanical Keyboard',
                'description': 'RGB mechanical keyboard with Cherry MX switches. Customizable lighting and macro support.',
                'original_price': 149.99,
                'minimum_price': 79.99,
                'discount_percentage': 45,
                'stock': 25
            },
            {
                'name': 'Portable SSD 1TB',
                'description': '1TB portable SSD with 550MB/s read speed. Compact and durable design with password protection.',
                'original_price': 129.99,
                'minimum_price': 69.99,
                'discount_percentage': 40,
                'stock': 30
            },
            {
                'name': 'USB-C Hub',
                'description': '7-in-1 USB-C hub with HDMI, SD card reader, and 100W power delivery. Supports multiple displays.',
                'original_price': 79.99,
                'minimum_price': 39.99,
                'discount_percentage': 50,
                'stock': 40
            },
            {
                'name': 'Wireless Mouse',
                'description': 'Ergonomic wireless mouse with precision tracking. Long battery life and silent clicking.',
                'original_price': 49.99,
                'minimum_price': 19.99,
                'discount_percentage': 55,
                'stock': 50
            },
        ]

        # Clear existing products
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing products'))

        # Create new products
        created_count = 0
        for product_data in products_data:
            product = Product.objects.create(**product_data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {product.name} - ₹{product.original_price}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully created {created_count} products!'))
