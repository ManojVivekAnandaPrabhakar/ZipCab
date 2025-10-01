#!/usr/bin/env bash

set -o errexit # Exit immediately if a command exits with a non-zero status.

# --- 1. Navigate to Django backend directory for Python dependencies ---
cd backend

# Install Python dependencies
pip install -r requirements.txt

# --- 2. Build React Frontend ---
# Navigate to the frontend directory
cd ../frontend

# Install Node dependencies (if needed, otherwise skip this line)
# npm install 

# Build the React app (creates the 'dist' directory inside 'frontend/')
npm run build



# Remove previous React build if necessary and copy new files
# This copies the contents of frontend/dist/ into backend/static
rm -rf static/frontend_build
mkdir -p static/frontend_build
cp -r ../frontend/dist/* static/frontend_build/

# *** IMPORTANT: You must update your Django settings.py to include 'static/frontend_build' 
#     in your STATICFILES_DIRS for collectstatic to pick them up.

# --- 4. Run Django Setup ---

# Run migrations (assuming manage.py is now in the current directory: backend/)
python manage.py migrate

# Collect static files (moves files from static/frontend_build/ into STATIC_ROOT)
python manage.py collectstatic --noinput

# Create admin user
python manage.py create_admin

# Navigate back to the project root for the start command
cd ..