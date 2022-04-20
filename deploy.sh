#!/usr/bin/env bash
# Set version variable
oldversion=$(cat .version)
export VERSION=$1

cd /apps/choralcat
# Pull latest code
echo "Pulling latest code from master..."
git fetch
echo "Checking out commit ${VERSION}..."
git checkout $VERSION

# Pulling latest docker images
echo "Pulling down latest docker images for version ${VERSION}..."
docker pull jerkeeler/choralcat:app-$VERSION
docker pull jerkeeler/choralcat:caddy-$VERSION

# Shutting down current services
echo "Shutting down old docker images on version ${oldversion}"
VERSION="${oldversion}" docker-compose down

# Migrating database
echo "Migrating the database..."
docker-compose run app .venv/bin/python manage.py migrate

# Restart the services
echo "Starting up services on version ${VERSION}"
docker-compose up -d

#
# Write new version
echo "${VERSION}" > .version

echo "Deploy complete!"
