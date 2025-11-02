# 🚗 AUTOINFO - Vehicle History Reports

Professional vehicle history report platform for US and Canadian vehicles.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis (optional, for caching)

### 2. Installation
```bash
# Clone or download project
cd autoinfo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
nano .env  # Edit database credentials
```

### 3. Database Setup
```bash
# PostgreSQL
sudo -u postgres psql
CREATE DATABASE autoinfo;
CREATE USER autoinfo_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE autoinfo TO autoinfo_user;
\q
```

### 4. Django Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 5. Run Development Server
```bash
python manage.py runserver
```

**✅ Open:** http://localhost:8000

**✅ Admin:** http://localhost:8000/admin

## 📁 Project Structure
```
autoinfo/
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
└── apps/
    ├── __init__.py
    └── core/
        ├── __init__.py
        ├── apps.py
        ├── models.py      # 5 database models
        ├── views.py       # 15+ views
        ├── urls.py
        ├── forms.py
        ├── api.py
        ├── admin.py
        ├── signals.py
        ├── tests.py
        ├── templates/
        │   └── core/
        │       ├── base.html
        │       ├── index.html
        │       ├── dashboard.html
        │       └── ...
        └── static/
            └── core/
                ├── css/
                │   └── style.css
                ├── js/
                │   └── main.js
                └── images/
```

## 🎯 Features

✅ User registration & authentication
✅ Balance management
✅ VIN search & reports
✅ Carfax, Autocheck, NMVTIS integration
✅ Payment processing (Stripe ready)
✅ Report packages (1, 10, 100)
✅ Admin panel
✅ API logging
✅ Responsive design

## 🔧 Configuration

Edit `.env` file:
- Database credentials
- API keys (Carfax, Autocheck, NMVTIS)
- Stripe keys
- Email settings

## 📝 Testing
```bash
python manage.py test
```

## 🚀 Production Deployment
```bash
# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 📞 Support

Email: support@autoinfo.com

---

**Made with ❤️ by AutoInfo Team**
