import time
from bs4 import BeautifulSoup
import logging
import asyncio
from aiohttp import ClientSession
from urllib.parse import parse_qs, urlparse


from config import LINKEDIN_DELAY, LINKEDIN_BETWEEN_PAGES, LINKEDIN_TIMEOUT, LINKEDIN_MAX_PAGES

from utils.helpers import linkedin_api_url, clean_url_params
from interfaces.notification import Notification
from interfaces.jobs import Job
from interfaces.status import Status

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class Search:
    def __init__(self, keyword: str, current_job_id: int, webhook: str, source_label: str, location: str = None, level: str = None, timeframe: str = None, job_type: str = None, work_enviornment: str = None, salary: str = None):
        # Declare search filters
        self.keyword = keyword
        self.current_job_id = current_job_id
        self.location = location
        self.level = level
        self.timeframe = timeframe
        self.job_type = job_type
        self.work_enviornment = work_enviornment
        self.salary = salary

        # Notification settings
        self.webhook = webhook
        self.source_label = source_label
        self.source = "https://www.linkedin.com/"
        self.db: dict[str, Job] = {}

        # Request config
        self.timeout = LINKEDIN_TIMEOUT
        self.headers = {
            'authority': 'www.linkedin.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

    async def get_job_listing(self, url: str, headers: dict):
        '''
        Enrich job data by parsing the job page
        '''
        async with ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                page_content = await resp.text()

        soup = BeautifulSoup(page_content, 'lxml')
        try:
            linkedin_url = soup.find(
                'a', class_='sign-up-modal__company_webiste')['href']
            parsed_url = urlparse(linkedin_url)
            raw_job_url_encoded = parse_qs(parsed_url.query)['url'][0]
            job_application = clean_url_params(raw_job_url_encoded)
        except Exception as e:
            job_application = url

        try:
            description = soup.find(
                'div', {'class': 'description__text description__text--rich'}).text.strip()
        except Exception as e:
            logging.error(
                f"Failed to parse description in {self.source_label}: {e}")
            description = None

        job_data = {
            'description': description,
            'application': job_application,
        }
        return job_data

    async def get_job(self, raw_job_html: BeautifulSoup) -> Job:
        """
        Returns a job object from the raw html off of search page
        """
        try:
            application_url = raw_job_html.find(
                'a', class_='base-card__full-link')['href']
        except:
            logging.error(
                f"Failed to parse application url in {self.source_label}")
            return

        job_data = await self.get_job_listing(application_url, self.headers)
        application, description = job_data[
            'application'], job_data['description']

        # TODO: add some sort of logging so we can instantly know if things are failing
        try:
            title = raw_job_html.find(
                'h3', class_='base-search-card__title').text.strip()
        except:
            logging.error(f"Failed to parse title in {self.source_label}")
            return

        try:
            company = raw_job_html.find(
                'a', class_='hidden-nested-link').text.strip()
        except:
            logging.error(
                f"Failed to parse company in {self.source_label}")
            return

        try:
            location = raw_job_html.find(
                'span', class_='job-search-card__location').text.strip()
        except:
            logging.error(
                "Failed to parse location in {self.source_label}")
        try:
            posted = raw_job_html.find(
                'time', class_='job-search-card__listdate')
            if posted is None:
                posted = raw_job_html.find(
                    'time', class_='job-search-card__listdate--new')
            posted_text = posted.text.strip() if posted else None
        except:
            posted = None
            logging.error(f"Failed to get posted date for {title}")

        job = Job(title, company, location, job_data['application'])

        try:
            job.set_date_posted(str(posted_text))
        except Exception as e:
            logging.error(
                f"Failed to convert posted date for {title}: {e}")

        job.set_description(description)
        job.set_application(application)

        return job

    async def scrape_page(self, mode: str, offset: int = 0):
        '''
        # TODO:
        - do not block on each job, create each job as a task and await all tasks (will require proxies)
        - add a timeout to each request
        '''
        # encode params into url
        search = linkedin_api_url(
            self.keyword, self.location, offset, self.level, self.timeframe, self.job_type, self.work_enviornment, self.salary)
        start_time = time.time()

        print(search)

        async with ClientSession(headers=self.headers) as session:
            async with session.get(search, allow_redirects=True) as resp:
                page_content = await resp.text()

        soup = BeautifulSoup(page_content, 'lxml')

        # if there are no li elements, we hit the end of the search results
        if len(soup.find_all('li')) == 0:
            logging.info(
                f"Finished scraping {self.source_label} {self.keyword}")
            self.status = Status.SUCCESS
            return

        try:
            jobs = soup.find_all('li')
        except Exception as e:
            logging.error(
                f"Error in {self.source_label} {self.keyword} scrape: {e}")
            return

        for job in jobs:
            try:
                job: Job = await self.get_job(job)
            except Exception as e:
                logging.error(
                    f"Error in {self.source_label} {self.keyword} scrape: {e}")
                continue

            if job is None:
                continue

            id_ = job.identifier()

            if mode != "start":
                if id_ not in self.db:
                    self.db[id_] = job
                    logging.info(f"New job found: {id_}")
                    notification = Notification(
                        job, self.webhook, self.source, self.source_label)

                    # thread notification
                    asyncio.create_task(notification.async_send())
            else:
                self.db[id_] = job
                # logging.info(
                #     f"[{time.time() - start_time} s] Job detected, storing: {id_}")

        logging.info(
            f"[{time.time() - start_time} s] Collected {len(jobs)} {self.source_label} {self.keyword} offset {offset}")
        logging.info(f"Total jobs found: {len(self.db)}")

    async def process_pages(self, mode):
        page = 0
        offset = 0
        while page <= LINKEDIN_MAX_PAGES and self.status == Status.IN_PROGRESS:
            await self.scrape_page(mode, offset)
            await asyncio.sleep(LINKEDIN_BETWEEN_PAGES)
            offset += 25
            page += 1

    async def start(self):
        mode = "start"
        logging.info(f"Starting {self.source_label} in {mode} mode")
        tries = 0
        self.status = Status.IN_PROGRESS

        while mode != "update":
            tries += 1
            await self.process_pages(mode)

            if len(self.db) > 0:
                mode = "update"
            elif tries == 3:
                logging.info("Failed to scrape 3 times, exiting")
                return

        logging.info(f"Starting {self.source_label} in {mode} mode")

        while True:
            self.status = Status.IN_PROGRESS
            await self.process_pages(mode)
            await asyncio.sleep(LINKEDIN_DELAY)
