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
