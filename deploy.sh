#!/usr/bin/env bash
cd /apps/choralcat
# Pull latest code
echo "Pulling latest code from master..."
git fetch
echo "Checking out commit $1..."
git checkout $1
# Install new dependencies and migrate database
echo "Installing python dependencies..."
.venv/bin/pip install -e .
echo "Migrating the database..."
.venv/bin/python manage.py migrate
# Untar staticfiles and delete tarball
echo "Unbundling static files..."
tar -xvf staticfiles.tar staticfiles/
rm staticfiles.tar
# Restart gunicorn
echo "Restarting services..."
sudo systemctl restart gunicorn
echo "Deploy complete!"
