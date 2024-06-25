from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode, unquote


def get_level_param(level: str):
    '''
    Create mapping return the correct level param for the given level
    '''
    level_map = {
        'internship': '1',
        'entry level': '2',
        'associate': '3',
        'senior': '4',
        'director': '5',
        'executive': '6',
    }
    return level_map[level.lower()] if level.lower() in level_map else ''


def get_date_range(timeframe: str):
    date_map = {
        'past month': 'r2592000',
        'past week': 'r604800',
        '24hr': 'r86400',
    }
    return date_map[timeframe.lower()] if timeframe.lower() in date_map else ''


def get_job_type(job_type: str):
    job_map = {
        'full time': 'F',
        'part time': 'P',
        'contract': 'C',
        'temporary': 'T',
        'volunteer': 'V'
    }
    return job_map[job_type.lower()] if job_type.lower() in job_map else ''


def get_work_enviornment(work_enviornment: str):
    work_enviornment_map = {
        'on-site': '1',
        'on site': '1',
        'remote': '2',
        'hybrid': '3'
    }
    return work_enviornment_map[work_enviornment.lower()] if work_enviornment.lower() in work_enviornment_map else ''


def get_salary_range(salary: str):
    salary_map = {
        '40000': '1',
        '60000': '2',
        '80000': '3',
        '100000': '4',
        '120000': '5',
    }
    return salary_map[salary.lower()] if salary.lower() in salary_map else ''


def linkedin_api_url(keyword: str, location: str, start: int, level: str, timeframe: str, job_type: str, work_enviornment: str, salary: str):
    url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?'

    keyword = keyword.replace(' ', '%20')
    url += f'keywords={keyword}'

    if location != '':
        url += f"&location={location}"
    if timeframe != '':
        url += f"&f_TPR={get_date_range(timeframe)}"
    if salary != '':
        url += f"&f_SB2={get_salary_range(salary)}"
    if level != '':
        url += f"&f_E={get_level_param(level)}"
    if work_enviornment != '':
        url += f"&f_WT={get_work_enviornment(work_enviornment)}"
    if job_type != '':
        print('job type', job_type)
        url += f"&f_JT={get_job_type(job_type)}"
    if start != 0:
        url += f"&start={start}"
    return url


def clean_url_params(url):
    url_parts = urlsplit(url)
    query_params = parse_qs(url_parts.query)
    filtered_params = {key: value for key, value in query_params.items() if all(substring not in key.lower(
    ) for substring in ['linkedin', 'utm_source', 'utm_medium']) and not any("linkedin" in val.lower() for val in value)}
    url_parts = url_parts._replace(
        query=urlencode(filtered_params, doseq=True))
    return unquote(urlunsplit(url_parts))
