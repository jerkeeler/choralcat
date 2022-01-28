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

Redis
```bash
# Start redis server locally
#To restart redis after an upgrade:
  brew services restart redis
#Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/redis/bin/redis-server /opt/homebrew/etc/redis.conf
```

Celery
```bash
# Run celery locally
celery -A choralcat worker --loglevel=INFO
```

```bash
# Run celery beat locally
celery -A choralcat beat -l INFO
```
