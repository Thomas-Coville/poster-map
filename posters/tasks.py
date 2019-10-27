from celery import Celery
from dynaconf import settings
from models import Job
from generator import MapGen


celery = Celery(__name__, autofinalize=False)

@celery.task
def say_hello(dude):
    print(f'hello {dude} !')
    return f"foooo {dude} !"

# @celery.task
# def add(x,y):
#     return x + y

# @celery.task
# def execute_job(jobId):
#     job = Job.objects.get(id=jobId)
#     gen = MapGen(job.latitude, job.longitude)
#     gen.execute()
#     pass