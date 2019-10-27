
from models import Job
from tasks import say_hello

class JobsService(object):
        
    def create_job(self, latitude, longitude):
        job = Job(
            latitude = latitude,
            longitude = longitude
        ).save()

        print('FOOOOOOOOOOOOOOOOOOOOOO')


        say_hello.delay('thomas')

        return job