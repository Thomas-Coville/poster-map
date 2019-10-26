import mongoengine

class Job(mongoengine.Document):
    width = mongoengine.IntField()
    height = mongoengine.IntField()
    latitude = mongoengine.FloatField()
    longitude = mongoengine.FloatField()
    zoom = mongoengine.IntField()