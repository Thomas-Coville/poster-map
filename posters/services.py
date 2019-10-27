
from models import Job
from tasks import say_hello

class JobsService(object):
    
    @staticmethod
    def create_job(latitude, longitude):
        job = Job(
            latitude = latitude,
            longitude = longitude
        ).save()

        print('FOOOOOOOOOOOOOOOOOOOOOO')


        say_hello.delay('thomas')

        return job