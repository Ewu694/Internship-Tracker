'''
Represents the Firestore database Client

Opertions:
- Add job
- Get all jobs
'''


class FirestoreClient:
    def __init__(self, job_colelction):
        self.db = firestore.Client()
        self.collection = self.db.collection(job_colelction)

    def add_job(self, job):
        self.collection.document(job.identifier()).set(job.to_dict())

    def get_all_jobs_as_dict(self):
        '''
        Return all jobs as a dictionary. dict[application] = job
        '''
        jobs = {}
        for job in self.collection.stream():
            jobs[job.application] = job.to_dict()
        return jobs
