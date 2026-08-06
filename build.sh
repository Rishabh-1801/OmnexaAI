#!/usr/bin/env bash
# ── Build script for Render.com deployment ──

set -o errexit

# Signal to settings.py that we are in build phase (DATABASE_URL may not be set yet)
export IS_RENDER_BUILD=true

echo ">>> Installing dependencies..."
pip install -r requirements.txt

echo ">>> Collecting static files..."
python manage.py collectstatic --no-input

echo ">>> Running database migrations..."
python manage.py migrate

echo ">>> Build complete!"
