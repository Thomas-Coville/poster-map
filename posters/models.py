import mongoengine
from bson import ObjectId
import marshmallow as ma

ma.Schema.TYPE_MAPPING[ObjectId] = ma.fields.String

class JobSchema(ma.Schema):
    id = ma.fields.String()
    class Meta:
        # Fields to expose
        fields = ("id","width")

class Job(mongoengine.Document):

    _schema = JobSchema()

    width = mongoengine.IntField()
    height = mongoengine.IntField()
    latitude = mongoengine.FloatField()
    longitude = mongoengine.FloatField()
    zoom = mongoengine.IntField()

    def dump(self):
        return self._schema.dump(self)