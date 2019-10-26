from marshmallow import Schema, fields, post_load
from bson import ObjectId
import mongoengine
import marshmallow_mongoengine as ma

Schema.TYPE_MAPPING[ObjectId] = fields.String

class Job(mongoengine.Document):
    width = mongoengine.IntField(default=2000)
    height = mongoengine.IntField(default=2000)
    latitude = mongoengine.FloatField(required=True)
    longitude = mongoengine.FloatField(required=True)
    zoom = mongoengine.IntField(default=5)

class JobSchema(ma.ModelSchema):
    class Meta:
         model = Job
         strict=True
