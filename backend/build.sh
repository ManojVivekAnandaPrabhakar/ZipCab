#!/usr/bin/env bash
set -o errexit  # Exit immediately if a command exits with a non-zero status

echo "🚀 Starting build process..."

# 1. Install backend dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 2. Build React frontend
echo "🧱 Building React frontend..."
cd ../frontend
npm install
npm run build

# 3. Move built files to Django static directory
echo "📂 Moving built frontend to Django static directory..."
cd ../backend
rm -rf static/frontend_build
mkdir -p static/frontend_build
cp -r ../frontend/dist/* static/frontend_build/

# 4. Run Django migrations and collectstatic
echo "⚙️ Running Django setup..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 5. Optional: Create default admin user (only if your management command exists)
if python manage.py | grep -q create_admin; then
  echo "👤 Creating admin user..."
  python manage.py create_admin
fi

echo "✅ Build complete!"
