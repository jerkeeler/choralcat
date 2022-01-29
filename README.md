# [choralcat](https://choralcat.org)

This repo contains the code that runs [choralcat.org](https://choralcat.org). 
Choralcat is a choral music management system. It is designed for easy
cataloguing, searching, and sorting of choral music. A user builds out their
library of choral music and is then provided with the tools to analyze it and
create programs of music it.

## Development

### Requirements

- Redis (not needed if not using celery)
  - Ensure that authentication is enabled and password is generated, put the password in the .env file
- Python 3.10
- Node v14

### Setup

1. Clone this repo
2. Create a python virtual environment
3. Install dependencies `make install`
4. Copy `.env.example` to `.env` and fill in actual values
   - All example values should be fine for local development, except if you want to test celery. To test celery locally you must provide a valid REDIS_PASSWORD.
5. Migrate your database `./manage migrate`
6. Create a superuser for testing `./manage createsuperuser`
7. Start a separate terminal session and start the JS/CSS development with `npm run dev`
8. Run the Django development server with `./manage.py runserver`
9. Enjoy and start development! Try visiting [localhost:8000](http://localhost:8000) and explore the app!

### Code Formatting

All Python code should be formatted with [Black](https://github.com/psf/black). 
JavaScript code is not currently automatically formatted.

### Commands

#### Staticfiles

```bash
# create JS bundle
npm run prod
# collect static files
./manage.py collectstatic
# create tarball
tar -cvf staticfiles.tar staticfiles/
# scp tarball
scp staticfiles.tar ip:/apps/choralcat/
# untar
tar -xvf staticfiles.tar staticfiles/
```

#### Redis

```bash
# Start redis server locally
#To restart redis after an upgrade:
brew services restart redis
#Or, if you don't want/need a background service you can just run:
/opt/homebrew/opt/redis/bin/redis-server /opt/homebrew/etc/redis.conf
```

#### Celery

```bash
# Run celery locally
celery -A choralcat worker --loglevel=INFO
```

```bash
# Run celery beat locally
celery -A choralcat beat -l INFO
```

## Deployment

This repo is equipped with CI/CD via GitHub Actions ([view workflow](./.github/workflows/choralcat-actions.yaml)). Tests are run on every
branch push to GitHub and pushes to the `main` branch are automatically deployed
to the site (only if tests pass). The site currently runs on a DigitalOcean droplet.
The current flow generates static files and transfers them to the server using `scp`
and then runs the [deploy script](./deploy.sh) on the server over ssh.

