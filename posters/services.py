
from models import Job
from image_generator import MapGen

class JobsService(object):
    
    @staticmethod
    def create_job(latitude, longitude, height = 2000, width = 2000, zoom = 5):
        job = Job(
            latitude = latitude,
            longitude = longitude,
            height = height, 
            width = width,
            zoom = zoom
        ).save()

        JobsService.execute_job(job)

        return job

    @staticmethod
    def execute_job(job):
        gen = MapGen()
        
        gen.generateImage()

        pass
        