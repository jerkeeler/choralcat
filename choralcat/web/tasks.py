import logging
import os
import sqlite3
from datetime import datetime, timedelta
from glob import glob
from typing import Any

from celery import Task, shared_task
from django.conf import settings

logger = logging.getLogger(__name__)
DATA_DIR = os.path.join(settings.BASE_DIR, "data")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
BACKUP_FILENAME_DATEFORMAT = "%Y-%m-%dT%H%M"
BACKUP_FILENAME = "db_backup_{now:{dateformat}}.sqlite3"
BACKUP_RETENTION_DAYS = 7


@shared_task(bind=True)
def choralcat_debug(self: Task, _: Any) -> None:
    logger.info(f"Request: {self.request!r}")


@shared_task
def backup_sqlite_database() -> None:
    def progress(_: Any, remaining: int, total: int) -> None:
        logger.info(f"Copied {total - remaining} of {total} pages...")

    logger.info("Starting new database backup")
    now = datetime.utcnow()
    backup_name = BACKUP_FILENAME.format(now=now, dateformat=BACKUP_FILENAME_DATEFORMAT)
    con = sqlite3.connect(os.path.join("data", "db.sqlite3"))
    bck = sqlite3.connect(os.path.join("data", "backups", backup_name))
    with bck:
        con.backup(bck, pages=1, progress=progress)
    bck.close()
    con.close()
    logger.info(f"Database backup complete. Database backup: {backup_name}")


@shared_task
def cleanup_sqlite_backups() -> None:
    now = datetime.utcnow()
    logger.info("Removing backups more than a week old")
    all_backups = glob(os.path.join(BACKUP_DIR, "*.sqlite3"))
    seven_days_ago = now - timedelta(days=BACKUP_RETENTION_DAYS)
    for backup in all_backups:
        basename = os.path.basename(backup)
        db_date = datetime.strptime(basename[10:-8], BACKUP_FILENAME_DATEFORMAT)
        if db_date < seven_days_ago:
            logger.info(f"Removing {basename}")
            os.remove(backup)
    logger.info("Finished cleaning up backups")
