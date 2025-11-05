#!/usr/bin/env bash
set -o errexit  # Exit immediately if any command fails

echo "🚀 Starting build process..."

# 1️⃣ Install Python dependencies
echo "📦 Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 2️⃣ Build the React frontend
echo "🧱 Building React frontend..."
cd ../frontend

# Ensure we’re in the correct directory (important if Render runs script from root)
if [ ! -f "package.json" ]; then
  echo "❌ Could not find package.json. Are you in the right directory?"
  exit 1
fi

npm ci --silent
npm run build

# 3️⃣ Move back to backend directory
cd ../backend

# 4️⃣ Django setup: migrate & collect static files
echo "⚙️ Applying migrations and collecting static files..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 5️⃣ Optional: Create admin (if management command exists)
if python manage.py | grep -q "create_admin"; then
  echo "👤 Creating admin user..."
  python manage.py create_admin
fi

echo "✅ Build complete! Ready for deployment."
