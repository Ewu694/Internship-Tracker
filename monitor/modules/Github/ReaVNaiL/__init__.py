import time
from bs4 import BeautifulSoup
import logging
from threading import Thread

from config import GITHUB_DELAY

from interfaces.notification import Notification
from interfaces.jobs import Job
from utils.scrape import get

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class ReaVNaiL:
    def __init__(self, github_url: str, webhook: str, source_label: str):
        self.github_url = github_url
        self.webhook = webhook
        self.source_label = source_label
        self.db: dict[str, Job] = {}
        self.headers = {
            'authority': 'github.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
        }

    def scrape(self, mode):
        page_content = get(self.github_url).text
        soup = BeautifulSoup(page_content, 'lxml')
        try:
            job_table = soup.find('tbody')
        except Exception as e:
            logging.error(f"Error in scrape: {e}")
            return
        for entry in job_table.find_all("tr"):
            try:
                if "no longer" in str(entry).lower():
                    #logging.info("No longer accepting applications")
                    continue
                if "not open" in str(entry).lower():
                    #logging.info("Not open yet")
                    continue
                elements = entry.find_all("td")
                if len(elements) != 5:
                    #logging.error("Invalid number of elements in table")
                    continue

                company = elements[0].text
                location = elements[1].text
                role = elements[2].text
                try:
                    application = elements[2].a['href']
                except:
                    application = self.github_url + f"?{role}+{company}"
            except Exception as e:
                logging.error(f"Error in parsing : {e}")
                continue
            job = Job(role=role, company=company,
                      location=location, application=application)
            id_ = job.identifier()
            if mode != "start":
                if id_ not in self.db:
                    self.db[id_] = job
                    logging.info(f"New job found: {str(job)}")
                    notification = Notification(
                        job, self.webhook, self.github_url, self.source_label)

                    # thread notification
                    Thread(target=notification.send).start()
            else:
                self.db[id_] = job
                logging.info(f"Job detected, storing: {str(job)}")

        logging.info(f"Found {len(self.db)} jobs on {self.source_label}")

    def start(self):
        mode = "start"
        logging.info(f"Starting {self.source_label} in {mode} mode")
        tries = 0
        while mode != "update":
            tries += 1
            self.scrape(mode)
            if len(self.db) > 0:
                mode = "update"
            if tries == 3:
                logging.info("Failed to scrape 3 times, exiting")
                return

        while True:
            self.scrape(mode)
            time.sleep(GITHUB_DELAY)
