"""
Script to populate database with sample products for testing
Run with: python manage.py shell < populate_products.py
"""

from shop.models import Product

# Create sample products with negotiable prices
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
    {
        'name': 'Gaming Monitor 27"',
        'description': '27-inch 144Hz gaming monitor with 1ms response time. IPS panel with vibrant colors and AMD FreeSync.',
        'original_price': 349.99,
        'minimum_price': 199.99,
        'discount_percentage': 42,
        'stock': 8
    },
    {
        'name': 'Mechanical Numpad',
        'description': 'RGB mechanical numpad with hot-swappable switches. Perfect for accountants and data entry professionals.',
        'original_price': 89.99,
        'minimum_price': 49.99,
        'discount_percentage': 44,
        'stock': 18
    },
    {
        'name': 'Cooling Pad Laptop',
        'description': 'Laptop cooling pad with dual fans and adjustable height. USB-powered with quiet operation.',
        'original_price': 39.99,
        'minimum_price': 19.99,
        'discount_percentage': 50,
        'stock': 35
    },
    {
        'name': 'External Hard Drive 2TB',
        'description': '2TB external hard drive with fast USB 3.0 connection. Perfect for backup and storage.',
        'original_price': 89.99,
        'minimum_price': 49.99,
        'discount_percentage': 44,
        'stock': 22
    },
    {
        'name': 'Phone Stand Adjustable',
        'description': 'Adjustable phone stand compatible with all smartphones. Anti-slip base and rotating design.',
        'original_price': 29.99,
        'minimum_price': 14.99,
        'discount_percentage': 50,
        'stock': 45
    },
    {
        'name': 'Desk Lamp LED',
        'description': 'LED desk lamp with adjustable brightness and color temperature. Touch control and USB charging port.',
        'original_price': 59.99,
        'minimum_price': 29.99,
        'discount_percentage': 50,
        'stock': 28
    },
    {
        'name': 'Cable Organizer Set',
        'description': 'Cable organizer set with 5 pieces. Keep your desk organized and cables untangled.',
        'original_price': 24.99,
        'minimum_price': 12.99,
        'discount_percentage': 48,
        'stock': 60
    },
    {
        'name': 'Wireless Charger',
        'description': 'Fast wireless charger supporting 15W charging. Compatible with all Qi-enabled devices.',
        'original_price': 44.99,
        'minimum_price': 24.99,
        'discount_percentage': 44,
        'stock': 32
    },
    {
        'name': 'USB Hub 4-Port',
        'description': '4-port USB hub with high-speed data transfer. Compact design and powered operation.',
        'original_price': 34.99,
        'minimum_price': 17.99,
        'discount_percentage': 48,
        'stock': 38
    },
    {
        'name': 'Document Camera',
        'description': 'USB document camera for presentations and scanning. 5MP sensor with auto-focus capability.',
        'original_price': 159.99,
        'minimum_price': 79.99,
        'discount_percentage': 50,
        'stock': 12
    },
    {
        'name': 'Bluetooth Speaker',
        'description': 'Portable Bluetooth speaker with 360-degree sound. Waterproof and 12-hour battery life.',
        'original_price': 79.99,
        'minimum_price': 39.99,
        'discount_percentage': 50,
        'stock': 28
    },
    {
        'name': 'Laptop Stand',
        'description': 'Aluminum laptop stand with adjustable height. Compatible with all laptops up to 17 inches.',
        'original_price': 69.99,
        'minimum_price': 34.99,
        'discount_percentage': 50,
        'stock': 24
    },
    # Fashion products (men, women, child)
    {
        'name': "Men's Classic Tee",
        'description': 'Comfort-fit men\'s classic tee — everyday fashion essential in soft cotton.',
        'original_price': 24.99,
        'minimum_price': 12.99,
        'discount_percentage': 48,
        'stock': 120
    },
    {
        'name': "Men's Slim Jeans",
        'description': 'Fashion-forward slim fit jeans for men with stretch for comfort.',
        'original_price': 59.99,
        'minimum_price': 34.99,
        'discount_percentage': 42,
        'stock': 60
    },
    {
        'name': "Women's Summer Dress",
        'description': 'Lightweight summer dress — feminine fashion with breathable fabric and floral print.',
        'original_price': 49.99,
        'minimum_price': 29.99,
        'discount_percentage': 40,
        'stock': 80
    },
    {
        'name': "Women's Leather Handbag",
        'description': 'Premium leather handbag — elegant fashion accessory with roomy interior.',
        'original_price': 129.99,
        'minimum_price': 89.99,
        'discount_percentage': 31,
        'stock': 25
    },
    {
        'name': "Women's Slide Sandals",
        'description': 'Comfort slide sandals — summer fashion with cushioned footbed.',
        'original_price': 39.99,
        'minimum_price': 19.99,
        'discount_percentage': 50,
        'stock': 70
    },
    {
        'name': "Kid's Hoodie",
        'description': 'Cozy children\'s hoodie — playful fashion and warm fleece lining for kids.',
        'original_price': 34.99,
        'minimum_price': 17.99,
        'discount_percentage': 49,
        'stock': 90
    },
    {
        'name': "Kid's Sneaker",
        'description': 'Durable kid\'s sneaker — sporty fashion with flexible sole for playtime.',
        'original_price': 44.99,
        'minimum_price': 24.99,
        'discount_percentage': 44,
        'stock': 85
    },
    {
        'name': "Men's Quilted Jacket",
        'description': 'Lightweight quilted jacket — stylish men\'s outerwear for cooler days.',
        'original_price': 99.99,
        'minimum_price': 59.99,
        'discount_percentage': 40,
        'stock': 40
    },
    {
        'name': "Women's Cashmere Scarf",
        'description': 'Soft cashmere scarf — luxe fashion accessory that stays warm and elegant.',
        'original_price': 79.99,
        'minimum_price': 39.99,
        'discount_percentage': 50,
        'stock': 35
    },
    {
        'name': "Unisex Baseball Cap",
        'description': 'Classic unisex baseball cap — casual fashion item with adjustable strap.',
        'original_price': 19.99,
        'minimum_price': 9.99,
        'discount_percentage': 50,
        'stock': 150
    },
]

# Clear existing products
Product.objects.all().delete()

# Create new products
created_count = 0
for product_data in products_data:
    product = Product.objects.create(**product_data)
    created_count += 1
    print(f"✓ Created: {product.name} - ₹{product.original_price}")

print(f"\n✓ Successfully created {created_count} products!")
