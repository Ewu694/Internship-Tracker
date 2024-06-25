import datetime

from interfaces.jobs import Job
from utils.discord_hooks import Webhook


class Notification:
    def __init__(self, job: Job, webhook: str, source: str, source_label: str):
        self.job = job
        self.webhook = webhook
        self.source = source
        self.source_label = source_label
        self.recorded = datetime.datetime.now()

    def send(self):
        webhook = Webhook(self.webhook)
        webhook.set_title(
            title=f"{self.job.role} @ {self.job.company}", url=self.job.application)
        webhook.set_desc(
            desc=f"Posted on [{self.source_label}]({self.source})")
        webhook.set_footer(text=str(self.recorded))
        webhook.post()

    async def async_send(self):
        webhook = Webhook(self.webhook)
        webhook.set_title(
            title=f"{self.job.role} @ {self.job.company}", url=self.job.application)
        webhook.set_desc(
            desc=f"Posted on [{self.source_label}]({self.source})")
        webhook.set_footer(text=str(self.recorded))
        await webhook.async_post()
