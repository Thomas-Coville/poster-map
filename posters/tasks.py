from celery import Celery

celery = Celery(__name__, autofinalize=False)

@celery.task(bind=True)
def say_hello(self, dude):
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