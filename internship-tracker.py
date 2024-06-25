from threading import Thread
import asyncio
from modules.Github.coderQuad import CoderQuad
from modules.Github.ReaVNaiL import ReaVNaiL
from modules.Github.PittCSC import PittCSC
from modules.LinkedIn.Search import Search

from config import CODEQUAD_WEBHOOK, CODERQUAD_URL, CODERQUAD_SOURCE_LABEL
from config import REAVNAIL_WEBHOOK, REAVNAIL_URL, REAVNAIL_SOURCE_LABEL
from config import PITTCSC_WEBHOOK, PITTCSC_URL, PITTCSC_SOURCE_LABEL
from config import LINKED_IN_SEARCH_QUERIES


async def main():
    coderQuad = CoderQuad(
        github_url=CODERQUAD_URL,
        webhook=CODEQUAD_WEBHOOK,
        source_label=CODERQUAD_SOURCE_LABEL
    )
    Thread(target=coderQuad.start).start()

    reaVNaiL = ReaVNaiL(
        github_url=REAVNAIL_URL,
        webhook=REAVNAIL_WEBHOOK,
        source_label=REAVNAIL_SOURCE_LABEL
    )
    Thread(target=reaVNaiL.start).start()

    pittcsc = PittCSC(
        github_url=PITTCSC_URL,
        webhook=PITTCSC_WEBHOOK,
        source_label=PITTCSC_SOURCE_LABEL
    )
    Thread(target=pittcsc.start).start()
    tasks = []
    for query in LINKED_IN_SEARCH_QUERIES:
        search = Search(
            keyword=query['query'],
            current_job_id=query['currentJobId'],
            webhook=query['webhook'],
            source_label=query['source_label'],
            location=query['location'],
            level=query['level'],
            timeframe=query['timeframe'],
            job_type=query['job_type'],
            work_enviornment=query['work_enviornment'],
            salary=query['salary']
        )
        tasks.append(search.start())
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())