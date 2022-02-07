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
3. Install dependencies `make install_dev`
4. Copy `.env.example` to `.env` and fill in actual values
   - All example values should be fine for local development, except if you want to test celery. To test celery locally you must provide a valid REDIS_PASSWORD.
5. Migrate your database `./manage migrate`
6. Load fixture data `make load_testdata`
7. Start a separate terminal session and start the JS/CSS development with `npm run dev`
8. Run the Django development server with `./manage.py runserver`
9. Enjoy and start development! Try visiting [localhost:8000](http://localhost:8000) and explore the app!
   - Feel free to use `test_user` with `testpassword` (from fixtures) or create a super user with `./manage.py createsuperuser`

Optional (setup pre-commit):
1. (in your virtualenv) `pre-commit install`

### Code Formatting

All Python code should be formatted with [Black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/index.html).
JavaScript code is not currently automatically formatted.

[pre-commit](https://pre-commit.com/) is used to automatically run Black and format
files after committing. Please set it up (see [Setup](#setup)) so that committed
files are all formatted in the same style.

If code is not formatted, CI tests will fail and deploys will be blocked.

### Adding a new dependency

If it's a dev dependency add it to [requirements/dev-requirements.in](./requirements/dev-requirements.in) if it's both
a prod and dev dependency add it to [requirements/requirements.in](./requirements/requirements.in). Then
run `make requires` to run pip-compile and automatically update the requirements.txt files which pin
versions and are use for actually installing dependencies.

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

#### Celery

Celery is used for performing async tasks in choralcat. It currently does very
little, but is there for added flexibility in the future. Celery is set up to use
Redis as its backend.

```bash
# Run celery locally
celery -A choralcat worker --loglevel=INFO
```

```bash
# Run celery beat locally
celery -A choralcat beat -l INFO
```

#### Redis

```bash
# Start redis server locally
#To restart redis after an upgrade:
brew services restart redis
#Or, if you don't want/need a background service you can just run:
/opt/homebrew/opt/redis/bin/redis-server /opt/homebrew/etc/redis.conf
```

### Testing

test_user password is `test_password`.

To run unit tests use `make test` or `./manage.py test`

## Deployment

This repo is equipped with CI/CD via GitHub Actions ([view workflow](./.github/workflows/choralcat-actions.yaml)). Tests are run on every
branch push to GitHub and pushes to the `main` branch are automatically deployed
to the site (only if tests pass). The site currently runs on a DigitalOcean droplet.
The current flow generates static files and transfers them to the server using `scp`
and then runs the [deploy script](./deploy.sh) on the server over ssh.
