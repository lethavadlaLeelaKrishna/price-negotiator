# 🚀 QUICK START GUIDE

## Price Negotiating Chatbot - Get Started in 5 Minutes

---

## ⚡ Super Quick Start (Windows)

### Step 1: Navigate to Project
```powershell
cd c:\Users\DELL\Desktop\chatbot
```

### Step 2: Activate Environment
```powershell
.\env\Scripts\activate
```

### Step 3: Start Server
```powershell
python manage.py runserver
```

### Step 4: Open Browser
```
http://localhost:8000
```

**Done! ✅ Start negotiating prices!**

---

## 📋 Detailed Setup (First Time)

### Requirements
- Python 3.8+ (check: `python --version`)
- Virtual environment (already created in `env/`)
- Internet connection (for CDN resources)

### Installation Steps

#### 1. Navigate to Project
```powershell
cd c:\Users\DELL\Desktop\chatbot
```

#### 2. Activate Virtual Environment
```powershell
# Windows
.\env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

You should see `(env)` in your terminal prompt.

#### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

Wait for installation to complete.

#### 4. Create Database
```powershell
python manage.py migrate
```

This creates all database tables.

#### 5. Create Admin Account
```powershell
python manage.py createsuperuser --username admin --email admin@chatbot.com
```

When prompted, enter a password (remember this!)

#### 6. Load Sample Products
```powershell
python manage.py populate_products
```

8 products will be added to the database.

#### 7. Start Development Server
```powershell
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

---

## 🌐 Access the Application

### URLs to Visit

| Page | URL |
|------|-----|
| Home | http://localhost:8000 |
| Product List | http://localhost:8000 |
| Admin Panel | http://localhost:8000/admin |

### Admin Login
**Username:** admin  
**Password:** (what you set during setup)

---

## 🎮 How to Use

### 1. Browse Products
- Open http://localhost:8000
- View product catalog
- Click "View Details" for more info

### 2. Start Negotiation
- Click "Start Negotiation" button
- Must be logged in (use admin/password)
- Opens chat interface

### 3. Make an Offer (Text)
- Enter price in the text field
- (Optional) Add message
- Click "Send Offer"
- Read bot's response
- If accepted → Add to cart
- If rejected → Try another price

### 4. Make an Offer (Voice)
- Click microphone button
 - Speak your offer (e.g., "I'll pay 800 rupees")
- Click stop
- Enter price in text field
- Submit

### 5. Add to Cart
- After negotiation accepted
- Set quantity
- Click "Add to Cart"

### 6. Checkout
- View cart: http://localhost:8000/cart/
- Click "Proceed to Checkout"
- Fill in details
- Complete purchase

### 7. View in Admin
- Go to admin panel
- View negotiations
- See chat history
- Monitor discounts

---

## 🐛 Troubleshooting

### Problem: Port 8000 Already in Use

**Solution:** Use a different port
```powershell
python manage.py runserver 8001
```

Then visit: http://localhost:8001

### Problem: "ModuleNotFoundError"

**Solution:** Reinstall dependencies
```powershell
pip install --upgrade -r requirements.txt
```

### Problem: "Database Error"

**Solution:** Reset database
```powershell
# Delete old database
del db.sqlite3

# Recreate everything
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@chatbot.com
python manage.py populate_products
```

### Problem: "Not logged in" error

**Solution:** 
1. Go to http://localhost:8000/admin/
2. Login with admin credentials
3. Go back to http://localhost:8000
4. Now try negotiating

### Problem: CSS/Icons not loading

**Solution:** 
```powershell
python manage.py collectstatic
```

### Problem: "ModuleNotFoundError: No module named 'django'"

**Solution:** Activate virtual environment
```powershell
.\env\Scripts\activate
```

Check that `(env)` appears in prompt.

### Problem: Server won't start

**Solution:** Check for errors
```powershell
python manage.py check
```

This shows what's wrong. Then fix and try again.

---

## 🔑 Admin Credentials

**When prompted during setup:**

```
Username: admin
Email: admin@chatbot.com
Password: [your choice]
```

Save the password! You'll need it to login.

### Recover Admin Access

If you forget password, reset database:
```powershell
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@chatbot.com
python manage.py populate_products
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `manage.py` | Django command runner |
| `db.sqlite3` | Database file |
| `requirements.txt` | Python dependencies |
| `chatbot/settings.py` | Django settings |
| `chatbot/urls.py` | URL routing |
| `shop/models.py` | Database models |
| `shop/views.py` | Views & APIs |
| `shop/negotiation_engine.py` | AI logic |
| `README.md` | Full documentation |

---

## 🎯 Project Structure

```
chatbot/                          ← Main project folder
├── manage.py                      ← Start here for commands
├── db.sqlite3                     ← Database (auto-created)
├── requirements.txt               ← Dependencies
├── README.md                      ← Full guide
├── FEATURE_SHOWCASE.md            ← Feature details
├── API_DOCUMENTATION.md           ← API reference
├── DEPLOYMENT_GUIDE.md            ← Production setup
│
├── chatbot/                       ← Settings folder
│   ├── settings.py               ← Configuration
│   ├── urls.py                   ← URL routes
│   └── wsgi.py
│
├── shop/                          ← Main app
│   ├── models.py                 ← Database models
│   ├── views.py                  ← Views & APIs
│   ├── admin.py                  ← Admin config
│   ├── negotiation_engine.py     ← AI logic
│   └── templates/                ← HTML templates
│
├── static/                        ← CSS, JS (auto-created)
├── media/                         ← User files (auto-created)
└── env/                           ← Python environment
```

---

## 💻 Commands Cheat Sheet

### Running the Server
```powershell
python manage.py runserver              # Default port 8000
python manage.py runserver 8001         # Custom port
python manage.py runserver 0.0.0.0:8000 # All interfaces
```

### Database Operations
```powershell
python manage.py migrate                # Apply migrations
python manage.py makemigrations         # Create migrations
python manage.py flush                  # Clear database
python manage.py dumpdata > data.json   # Backup data
```

### Create/Manage Users
```powershell
# Create superuser (admin)
python manage.py createsuperuser

# Change password
python manage.py changepassword admin

# Create regular user (via admin panel)
```

### Load Data
```powershell
python manage.py populate_products      # Load 8 sample products
python manage.py loaddata data.json     # Restore backup
```

### Utilities
```powershell
python manage.py check                  # System check
python manage.py shell                  # Python REPL with Django
python manage.py test                   # Run tests
python manage.py collectstatic          # Collect static files
```

---

## 🎨 Customization

### Change Product Data

Edit: `shop/management/commands/populate_products.py`

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
```

Then run:
```powershell
python manage.py populate_products
```

### Change Colors

Edit: `shop/templates/shop/base.html`

Find this section:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    /* ... */
}
```

Change hex values to your colors.

### Change AI Logic

Edit: `shop/negotiation_engine.py`

Find `_calculate_confidence_score()` method and adjust:
```python
if factors.get('offer_trend') == 'improving':
    score += 15  # Change this value
```

---

## 📞 Need Help?

### Check Documentation
- **README.md** - Full setup guide
- **FEATURE_SHOWCASE.md** - Feature details
- **API_DOCUMENTATION.md** - API reference
- **DEPLOYMENT_GUIDE.md** - Production setup

### Check Admin Panel
- http://localhost:8000/admin/
- View all negotiations
- Check chat history
- Monitor discounts

### Run System Check
```powershell
python manage.py check
```

### View Server Logs
Look at terminal output while server is running. Error messages appear there.

---

## 🚀 Next Steps

After setup:

1. ✅ Browse products at http://localhost:8000
2. ✅ Login at http://localhost:8000/admin/
3. ✅ Start negotiating!
4. ✅ Add items to cart
5. ✅ Complete checkout
6. ✅ View negotiations in admin

---

## 💡 Pro Tips

### Faster Testing
```powershell
# Terminal 1 - Keep server running
python manage.py runserver

# Terminal 2 - Run commands while server is up
python manage.py populate_products
```

### Debug Mode
In `chatbot/settings.py`, set `DEBUG = True` for detailed error pages.

### Check Database
```powershell
# Enter Django shell
python manage.py shell

# In Python shell:
>>> from shop.models import Product
>>> Product.objects.all().count()
8  # Should show 8 products
```

### Monitor Changes
```powershell
# Watch for file changes and auto-reload
python manage.py runserver --reload
```

---

## 📊 Sample Test Case

1. **Start server:**
   ```powershell
   python manage.py runserver
   ```

2. **Visit http://localhost:8000**

3. **Click on "Premium Laptop"**

4. **Click "Start Negotiation"**

5. **Try offers:**
    - First: ₹1100 (15% off) → Should ACCEPT ✅
    - First: ₹800 (38% off) → Should COUNTER 🔄
    - First: ₹500 (61% off) → Should REJECT ❌

6. **If accepted, click "Add to Cart"**

7. **View cart at http://localhost:8000/cart/**

8. **Click "Proceed to Checkout"**

9. **View negotiations in admin**

---

## 🎯 What's Working

✅ Product listing
✅ Product details
✅ Negotiation chatbot
✅ Text offers
✅ Voice recording (client-side)
✅ AI decision logic
✅ Shopping cart
✅ Checkout
✅ Admin panel
✅ Chat history
✅ Responsive design

---

## 🔐 Security

**For Development:**
- ✅ Everything working
- ✅ DEBUG mode on
- ✅ Insecure settings OK

**For Production:**
- ❌ Change `DEBUG = False`
- ❌ Update `SECRET_KEY`
- ❌ Set `ALLOWED_HOSTS`
- ❌ Use HTTPS
- ❌ Database password
- ❌ See DEPLOYMENT_GUIDE.md

---

## 📝 Notes

- All prices in INR (Indian Rupees)
- SQLite database (good for dev, PostgreSQL for production)
- Virtual environment at `env/`
- 8 sample products included
- Full admin access
- Mobile responsive

---

## 🎉 Ready to Start?

```powershell
cd c:\Users\DELL\Desktop\chatbot
.\env\Scripts\activate
python manage.py runserver
```

Then open: **http://localhost:8000** 🚀

---

**Happy Negotiating!** 💰💬

*Price Negotiating Chatbot v1.0 - Quick Start Guide*
