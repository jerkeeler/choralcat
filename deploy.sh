#!/usr/bin/env bash
cd /apps/choralcat
# Pull latest code
echo "Pulling latest code from master..."
git fetch
echo "Checking out commit $1..."
git checkout $1
# Install new dependencies and migrate database
echo "Installing python dependencies..."
make install
echo "Migrating the database..."
.venv/bin/python manage.py migrate
# Untar staticfiles and delete tarball
echo "Unbundling static files..."
tar -xvf staticfiles.tar staticfiles/
rm staticfiles.tar
# Restart gunicorn
echo "Restarting services..."
sudo systemctl restart gunicorn.service
sudo systemctl restart celery.service
sudo systemctl restart celerybeat.service
echo "Deploy complete!"
