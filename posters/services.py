
from models import Job
from generator import MapGen

class JobsService(object):
    
    @staticmethod
    def create_job(latitude, longitude):
        job = Job(
            latitude = latitude,
            longitude = longitude
        ).save()

        JobsService.execute_job(job.id)

        return job

    @staticmethod
    def execute_job(jobId):

        job = Job.objects.get(id=jobId)

        gen = MapGen(job.latitude, job.longitude)

        # gen.execute()

        pass
        