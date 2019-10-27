from models import Job
import tasks

class JobsService(object):
        
    @staticmethod
    def create_job(latitude, longitude):
        job = Job(
            latitude = latitude,
            longitude = longitude,
            status = "pending"
        ).save()            

        tasks.execute_job.delay(str(job.id))

        return job

    @staticmethod
    def getJobById(jobId):
        job = Job.objects.get(id=jobId)    
        return job