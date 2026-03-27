# 🎯 Price Negotiating Chatbot with Text & Voice
## AI-Powered E-Commerce Price Negotiation System

A modern Django-based e-commerce application featuring an intelligent chatbot that negotiates product prices through text and voice interactions. Customers can offer lower prices, and the AI decides whether to accept, reject, or make counter-offers based on intelligent decision logic.

---

## 📋 Features

### ✅ Core Features

| Feature | Explanation |
|---------|------------|
| **Price Negotiation** | Users can offer lower prices and the chatbot intelligently decides acceptance based on AI logic |
| **Text Interaction** | Standard chat interface for real-time price negotiations with emoji feedback |
| **Voice Interaction** | Speak price offers; bot responds with audio support (client-side speech recognition ready) |
| **AI Decision Logic** | Machine learning/rule-based evaluation of discounts considering multiple factors |
| **User Intent Understanding** | Detects when customers are bargaining and adjusts responses accordingly |
| **Secure Checkout Integration** | Final agreed price is transferred to cart and checkout with negotiation history |
| **Session Management** | Tracks negotiation sessions with full conversation history |
| **Admin Dashboard** | Manage products, view negotiations, analyze customer behavior |

### 🎨 UI/UX Features
- **Bootstrap 5 Styling** - Responsive, modern design
- **Font Awesome Icons** - 1000+ icons for better visual communication
- **Real-time Chat** - AJAX-based chat without page reload
- **Animated Transitions** - Smooth animations for messages and interactions
- **Mobile Responsive** - Works perfectly on desktop, tablet, and mobile
- **Dark-themed Gradient** - Eye-catching purple gradient design

---

## 🏗️ Project Architecture

### Database Models

```
Product
  ├── name (CharField)
  ├── description (TextField)
  ├── original_price (DecimalField)
  ├── minimum_price (DecimalField)
  ├── discount_percentage (IntegerField)
  └── stock (IntegerField)

NegotiationSession
  ├── user (ForeignKey to User)
  ├── product (ForeignKey to Product)
  ├── session_id (CharField, unique)
  ├── status (Active/Accepted/Rejected/Abandoned)
  ├── original_price
  ├── offered_price
  ├── final_agreed_price
  ├── discount_percentage
  └── created_at, updated_at

ChatMessage
  ├── session (ForeignKey to NegotiationSession)
  ├── message_type (user_text/user_voice/bot_text/bot_voice)
  ├── content (TextField)
  ├── audio_file (FileField, optional)
  ├── offered_price (DecimalField, optional)
  └── created_at

PriceOffer
  ├── session (ForeignKey to NegotiationSession)
  ├── offered_price (DecimalField)
  ├── discount_percentage (DecimalField)
  ├── status (pending/accepted/rejected/counter)
  ├── reason (TextField)
  ├── counter_offer_price (DecimalField, optional)
  └── created_at

Cart & CartItem
  ├── Stores negotiated prices from sessions
  ├── Tracks original vs negotiated prices
  └── Maintains negotiation session reference
```

### URL Routes

```
/                           - Product listing page
/product/<id>/              - Product detail page
/negotiate/<product_id>/    - Main negotiation chatbot interface
/shop/send-text-offer/      - API endpoint for text offers (POST)
/shop/send-voice-offer/     - API endpoint for voice offers (POST)
/shop/chat-history/         - Retrieve chat history (GET)
/shop/add-to-cart/          - Add negotiated item to cart (POST)
/cart/                       - View shopping cart
/checkout/                  - Checkout page
/admin/                     - Django admin panel
```

---

## 🤖 AI Decision Logic

The negotiation engine evaluates offers based on **multiple factors**:

### Decision Factors

1. **Price Bounds** - Is price above/below minimum acceptable?
2. **Discount Percentage** - Does it exceed maximum allowed discount?
3. **Negotiation History** - How many offers made? Are prices improving?
4. **Session Duration** - How long has user been negotiating?
5. **Offer Trend** - Is customer getting closer to acceptable price?
6. **Confidence Score** - Calculated from all factors (0-100)

### Decision Types

```python
ACCEPTED  → User's offer meets criteria, deal is done!
REJECTED  → Price too low, but may offer counter
COUNTER   → Suggesting a better price for both parties
```

### Example Logic Flow

```
Offered Price: ₹800 for ₹1299 item
→ Discount: 38.3%
→ Max Allowed: 30%
→ History: 3rd offer, improving trend
→ Duration: 8 minutes
→ Confidence Score: 65/100
→ Decision: COUNTER OFFER at ₹909.93 (30% off)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Download

```bash
cd c:\Users\DELL\Desktop\chatbot
```

### Step 2: Activate Virtual Environment

```bash
# Windows
.\env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Django==4.2.27
pip install djangorestframework==3.16.1
pip install django-cors-headers==4.9.0
```

### Step 4: Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser --username admin --email admin@chatbot.com

# Populate sample products
python manage.py populate_products
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

Server will start at: **http://localhost:8000**

---

## 📱 Usage Guide

### 1. Access the Application

1. Open browser to `http://localhost:8000`
2. Click on a product to view details
3. Click "Start Negotiation" button

### 2. Negotiate Price (Text Method)

```
1. Enter your price offer in the text field
2. (Optional) Add a message like "Best I can do"
3. Click "Send Offer"
4. Read bot's response
5. If accepted, add to cart
6. If counter, make new offer
```

### 3. Negotiate Price (Voice Method)

```
1. Click the microphone button
2. Speak your price offer clearly (e.g., "I'll pay 800 rupees")
3. Click microphone again to stop recording
4. Enter the price in the text field
5. Submit and wait for response
```

### 4. Checkout with Negotiated Price

```
1. Review cart with negotiated prices
2. Proceed to checkout
3. Enter shipping and payment details
4. Complete purchase
```

### 5. Admin Panel

Access at: `http://localhost:8000/admin/`

**Login with:**
- Username: `admin`
- Password: (Use the one you set during setup)

**Manage:**
- Products
- Negotiation Sessions
- Chat Messages
- Price Offers
- Shopping Carts

---

## 🎮 Sample Data

8 Tech Products Pre-loaded:

| Product | Original Price | Min Price | Max Discount | Stock |
|---------|---------------|-----------|-------------|-------|
| Premium Laptop | ₹1,299.99 | ₹899.99 | 30% | 5 |
| Smart Watch Pro | ₹399.99 | ₹249.99 | 35% | 12 |
| Wireless Headphones | ₹349.99 | ₹199.99 | 40% | 20 |
| 4K Webcam | ₹199.99 | ₹99.99 | 45% | 15 |
| Mechanical Keyboard | ₹149.99 | ₹79.99 | 45% | 25 |
| Portable SSD 1TB | ₹129.99 | ₹69.99 | 40% | 30 |
| USB-C Hub | ₹79.99 | ₹39.99 | 50% | 40 |
| Wireless Mouse | ₹49.99 | ₹19.99 | 55% | 50 |

---

## 📝 API Endpoints

### Text Offer Endpoint

```http
POST /shop/send-text-offer/<session_id>/
Content-Type: application/json

{
  "offered_price": 950.00,
  "message": "Best offer I can make"
}

Response:
{
  "status": "success",
  "offer_status": "counter|accepted|rejected",
  "bot_response": "Your message here",
  "counter_offer": 1100.00,
  "discount": 15.5
}
```

### Voice Offer Endpoint

```http
POST /shop/send-voice-offer/<session_id>/
Content-Type: multipart/form-data

FormData:
  - audio: [WAV/MP3 file]
  - offered_price: 950.00

Response:
{
  "status": "success",
  "offer_status": "counter|accepted|rejected",
  "bot_response": "Your message here",
  "message_id": 123
}
```

### Chat History Endpoint

```http
GET /shop/chat-history/<session_id>/

Response:
{
  "status": "success",
  "messages": [
    {
      "type": "user_text",
      "content": "My offer",
      "timestamp": "2025-12-09T10:30:00Z",
      "offered_price": 950.00
    },
    ...
  ]
}
```

---

## 🛠️ Configuration

### Django Settings (`chatbot/settings.py`)

**Add/Remove Apps:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'shop',  # Our app
]
```

**Static Files:**
```python
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Database:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 🎯 Customization

### Change Product Data

Edit `shop/management/commands/populate_products.py`:

```python
products_data = [
    {
        'name': 'Your Product',
        'description': 'Your description',
        'original_price': 999.99,
        'minimum_price': 599.99,
        'discount_percentage': 40,
        'stock': 10
    },
]

python manage.py populate_products
```

### Adjust AI Decision Logic

Edit `shop/negotiation_engine.py`:

```python
class PriceNegotiationEngine:
    def _calculate_confidence_score(self, decision_data, time_spent):
        score = 50  # Base score
        
        # Modify thresholds here
        if factors.get('offer_trend') == 'improving':
            score += 15  # Change this value
```

### Customize UI Styling

Edit `shop/templates/shop/base.html`:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    /* Customize colors */
}
```

---

## 🐛 Troubleshooting

### Issue: Port 8000 Already in Use

```bash
python manage.py runserver 8001
```

### Issue: Static Files Not Loading

```bash
python manage.py collectstatic
```

### Issue: Database Errors

```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_products
```

### Issue: Module Not Found

```bash
pip install -r requirements.txt
# or reinstall specific packages
pip install --upgrade djangorestframework
```

---

## 📦 Project Structure

```
chatbot/
├── chatbot/                    # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── shop/                       # Main app
│   ├── models.py              # Database models
│   ├── views.py               # Views & API endpoints
│   ├── admin.py               # Admin configuration
│   ├── negotiation_engine.py  # AI logic
│   ├── templates/shop/        # HTML templates
│   │   ├── base.html
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── negotiation_chatbot.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   └── checkout_success.html
│   ├── management/commands/
│   │   └── populate_products.py
│   └── migrations/            # Database migrations
├── static/                    # CSS, JS, images
├── media/                     # User uploaded files
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django CLI
└── README.md                  # This file
```

---

## 🔐 Security Notes

⚠️ **Important for Production:**

1. **Never use DEBUG=True in production**
2. **Change SECRET_KEY in settings.py**
3. **Use environment variables for sensitive data**
4. **Set secure password for admin user**
5. **Configure ALLOWED_HOSTS properly**
6. **Use HTTPS instead of HTTP**
7. **Set CORS_ALLOWED_ORIGINS to specific domains**

**Example Production Setup:**

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📊 Monitoring & Analytics

### View Negotiations in Admin

1. Go to Admin Panel
2. Click "Negotiation Sessions"
3. Filter by status, date, discount percentage
4. View chat history for each session

### Export Data

Use Django admin to export:
- Product performance
- Customer negotiation patterns
- Discount statistics
- Session analytics

---

## 🚀 Next Steps

### Potential Enhancements

1. **Voice Recognition** - Integrate Google Cloud Speech-to-Text
2. **Machine Learning** - Train model on real negotiations
3. **Recommendations** - Suggest products based on negotiation history
4. **Multi-language** - Support multiple languages
5. **Payment Integration** - Stripe, PayPal integration
6. **Email Notifications** - Order confirmations, status updates
7. **Analytics Dashboard** - Real-time metrics and charts
8. **Mobile App** - Native iOS/Android apps
9. **Wishlist Feature** - Save favorite negotiated prices
10. **Referral System** - Reward customers for referrals

---

## 📞 Support

For issues or questions:

1. Check the Troubleshooting section
2. Review Django documentation
3. Check application logs
4. Verify all dependencies are installed

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 🙌 Credits

Built with:
- **Django 4.2** - Web framework
- **Bootstrap 5** - UI framework
- **Font Awesome 6** - Icons
- **SQLite** - Database

---

**Happy Negotiating! 🎉💰**

*Price Negotiating Chatbot v1.0 - 2025*
