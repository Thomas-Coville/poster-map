from celery import Celery
from celery.signals import after_task_publish, before_task_publish


celery = Celery(__name__, autofinalize=False)


@after_task_publish.connect
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    info = headers if 'task' in headers else body
    print('after_task_publish for task id {info[id]}'.format(
        info=info,
    ))

@before_task_publish.connect
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    info = headers if 'task' in headers else body
    print('after_task_publish for task id {info[id]}'.format(
        info=info,
    ))

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