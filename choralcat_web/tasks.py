import os
import sqlite3
from datetime import datetime

from celery import shared_task


@shared_task(bind=True)
def choralcat_debug(self, x):
    print(f"Request: {self.request!r}")


@shared_task
def backup_sqlite_database():
    def progress(_, remaining, total):
        print(f"Copied {total - remaining} of {total} pages...")

    now = datetime.utcnow()
    backup_name = f"db_backup_{now:%Y-%m-%dT%H%M}.sqlite3"
    con = sqlite3.connect("db.sqlite3")
    bck = sqlite3.connect(os.path.join("backups", backup_name))
    with bck:
        con.backup(bck, pages=1, progress=progress)
    bck.close()
    con.close()
