from celery import shared_task


@shared_task(bind=True)
def choralcat_debug(self, x):
    print(f"Request: {self.request!r}")
