@echo off
REM Quick Start Script for Price Negotiating Chatbot (Windows)

echo.
echo ========================================
echo.  Price Negotiating Chatbot - Quick Start
echo.
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version

REM Create virtual environment if it doesn't exist
if not exist "env" (
    echo Creating virtual environment...
    python -m venv env
)

REM Activate virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Create superuser
echo Creating superuser (admin account)...
python manage.py createsuperuser --username admin --email admin@chatbot.com --noinput 2>nul || cls

REM Populate sample data
echo Populating sample products...
python manage.py populate_products

echo.
echo ========================================
echo. Setup complete!
echo.
echo Starting development server...
echo.
echo Server running at: http://localhost:8000
echo Admin panel at: http://localhost:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python manage.py runserver
pause
