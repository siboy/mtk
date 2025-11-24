#!/bin/bash
set -e

# Buat tabel database
echo "Creating database tables..."
python -c "
from app2 import app, db
with app.app_context():
    db.create_all()
print('✅ Tables created!')
"

# Start Nginx
echo "Starting Nginx..."
nginx

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 127.0.0.1:8867 \
              --workers 4 \
              --worker-class gevent \
              --worker-connections 1000 \
              --timeout 30 \
              --log-level info \
              app2:app