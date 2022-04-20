#!/usr/bin/env bash
# Set version variable
oldversion=$(cat .version)
export VERSION=$1

cd /apps/choralcat
# Pull latest code
echo "Pulling latest code from master..."
git fetch
echo "Checking out commit $1..."
git checkout $1
echo "$1" > .version
# Pulling latest docker images
echo "Pulling down latest docker images for version ${VERSION}..."
docker pull jerkeeler/choralcat:app-$1
docker pull jerkeeler/choralcat:caddy-$1

# Shutting down current services
echo "Shutting down old docker images on version ${oldversion}"
VERSION="${oldversion}" docker-compose down

# Migrating database
echo "Migrating the database..."
docker-compose run app .venv/bin/python manage.py migrate

# Restart the services
echo "Starting up services on version ${VERSION}"
docker-compose up -d

echo "Deploy complete!"
