import logging
import os
import sqlite3
from datetime import datetime

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def choralcat_debug(self, x):
    print(f"Request: {self.request!r}")


@shared_task
def backup_sqlite_database():
    def progress(_, remaining, total):
        print(f"Copied {total - remaining} of {total} pages...")

    logger.info("Starting new database backup")
    now = datetime.utcnow()
    backup_name = f"db_backup_{now:%Y-%m-%dT%H%M}.sqlite3"
    con = sqlite3.connect(os.path.join("data", "db.sqlite3"))
    bck = sqlite3.connect(os.path.join("data", "backups", backup_name))
    with bck:
        con.backup(bck, pages=1, progress=progress)
    bck.close()
    con.close()
    logger.info(f"Database backup complete. Database backup: {backup_name}")
