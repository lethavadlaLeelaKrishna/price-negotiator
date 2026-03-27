#!/bin/bash
# Quick Start Script for Price Negotiating Chatbot
# Run this to set up and start the application

echo "🚀 Price Negotiating Chatbot - Quick Start"
echo "=========================================="
echo ""

# Check Python
echo "✓ Checking Python installation..."
python --version

# Create virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "✓ Creating virtual environment..."
    python -m venv env
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source env/Scripts/activate
else
    # macOS/Linux
    source env/bin/activate
fi

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "✓ Running database migrations..."
python manage.py migrate

# Create superuser if needed
echo "✓ Creating superuser (admin account)..."
python manage.py createsuperuser --username admin --email admin@chatbot.com --noinput 2>/dev/null || true

# Populate sample data
echo "✓ Populating sample products..."
python manage.py populate_products

# Run server
echo ""
echo "🎉 Setup complete!"
echo "✓ Starting development server..."
echo ""
echo "Server running at: http://localhost:8000"
echo "Admin panel at: http://localhost:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
