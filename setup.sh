#!/bin/bash
echo "🚀 Setting up Liemo API..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env
echo "✅ Created .env file - please update DB_USER with your Mac username"

# Run migrations
python manage.py migrate

# Create superuser
echo "📝 Creating superuser..."
python manage.py createsuperuser

echo "✅ Setup complete! Run: python manage.py runserver"
