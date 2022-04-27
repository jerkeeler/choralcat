#!/usr/bin/env bash
cd /apps/choralcat

# Set version variables
export VERSION=$1
oldversion=$(cat .version)

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
make dock_down

# Migrating database
echo "Migrating the database..."
make dock_migrate

# Restart the services
echo "Starting up services on version ${VERSION}"
make dock_up

# Write new version
echo "${VERSION}" > .version

echo "Deploy complete!"
