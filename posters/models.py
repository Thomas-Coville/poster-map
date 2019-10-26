import mongoengine
from bson import ObjectId
import marshmallow as ma

ma.Schema.TYPE_MAPPING[ObjectId] = ma.fields.String


class JobSchema(ma.Schema):
    id = ma.fields.String()

    class Meta:
        # Fields to expose
        fields = ("id", "width", "height", "zoom", "latitude", "longitude")


class Job(mongoengine.Document):

    _schema = JobSchema()

    width = mongoengine.IntField(default=2000)
    height = mongoengine.IntField(default=2000)
    latitude = mongoengine.FloatField(required=True)
    longitude = mongoengine.FloatField(required=True)
    zoom = mongoengine.IntField(default=5)

    def dump(self):
        return self._schema.dump(self)
