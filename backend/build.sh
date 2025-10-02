#!/usr/bin/env bash

set -o errexit # Exit immediately if a command exits with a non-zero status.

# NOTE: The working directory is now 'ZipCab/backend/'

# --- 1. Install Python dependencies (already in backend directory) ---
pip install -r requirements.txt

# --- 2. Build React Frontend ---

# Navigate to the frontend directory (up one level, then into frontend)
cd ../frontend

npm install 
npm run build

# --- 3. Copy React Build to Django Static Folder ---

# Navigate back to the backend directory
cd ../backend

# Target: static/frontend_build is inside the current directory (backend/)
rm -rf static/frontend_build
mkdir -p static/frontend_build

# Source: ../frontend/dist/ is correct relative to the backend/ directory
cp -r ../frontend/dist/* static/frontend_build/

# --- 4. Run Django Setup ---

# manage.py is in the current directory: backend/
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_admin