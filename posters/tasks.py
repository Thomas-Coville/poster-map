from celery import Celery
from celery.signals import after_task_publish, before_task_publish
from generator import MapGen
from models import Job

celery = Celery('posters')


@celery.task
def execute_job(jobId):
    job = Job.objects.get(id=jobId)

    job.status = "started"

    job.save()

    gen = MapGen(job.latitude, job.longitude)
    # gen.execute(jobId)    

    job.status = "completed"
    job.save()
    