import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_DELAY = 60 * 5
LINKEDIN_DELAY = 60 * 5
LINKEDIN_BETWEEN_PAGES = 5
LINKEDIN_TIMEOUT = 5

CODEQUAD_WEBHOOK = "https://discord.com/api/webhooks/1126618173194649771/zNnnV-DO9Fo6PSuaQnNPR-cAcZmLcNwuVyPHRt6z8pkQDB-oATUfFqtPV9UUNLJ6hFnI"
CODERQUAD_URL = "https://github.com/coderQuad/New-Grad-Positions"
CODERQUAD_SOURCE_LABEL = "coderQuad/New-Grad-Positions"

REAVNAIL_WEBHOOK = "https://discord.com/api/webhooks/1126625556302155878/TxgLg1Z3MKG6AV8t9j0Tl4p0xIIisC2Wd6JVT-StRhjupgTTVChut5O4EMR3nr6kXkBS"
REAVNAIL_URL = "https://github.com/ReaVNaiL/New-Grad-2024"
REAVNAIL_SOURCE_LABEL = "ReaVNaiL/New-Grad-2024"

PITTCSC_WEBHOOK = "https://discord.com/api/webhooks/1126627561586294837/QByySjQGrd0IJO9dZDoS3BgzOKiGDmqCYThoUx4ISvwGhg-UY4rmFCd8fZSZDchwTuK6"
PITTCSC_URL = "https://github.com/SimplifyJobs/Summer2024-Internships"
PITTCSC_SOURCE_LABEL = "pittcsc/Summer2024-Internships"
LINKEDIN_MAX_PAGES = 10

# LINKED IN SEARCH QUERIES
LINKED_IN_SEARCH_QUERIES = [
    {
        "query": "software engineering",
        "currentJobId": 3637859377,
        "webhook": "https://discord.com/api/webhooks/1134271944863273053/-WKINiSbj52SuG391oYXjN_-QOeLf_QERXidSPPSRFcdFEUcgmlHAXJhflAhDD_dpWT_",
        "source_label": "LinkedIn Search",
        "location": "",
        "level": "Entry Level",
        "timeframe": "Past Week",
        "job_type": "",
        "work_enviornment": "",
        "salary": ""
    },
    {
        "query": "software engineering internship",
        "currentJobId": 3637859377,
        "webhook": "https://discord.com/api/webhooks/1134271813053075596/ep7fj8mxvjMsx73083x_fmWfj1u4C87ArVxDtZ5It9nGW8fyBAP7dMgMFo0bKLrsHc6w",
        "source_label": "LinkedIn Search",
        "location": "",
        "level": "Internship",
        "timeframe": "Past Week",
        "job_type": "",
        "work_enviornment": "",
        "salary": ""
    },
]
