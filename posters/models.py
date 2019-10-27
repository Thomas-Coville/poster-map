from marshmallow import Schema, fields, post_load
from bson import ObjectId
import mongoengine
import marshmallow_mongoengine as ma

Schema.TYPE_MAPPING[ObjectId] = fields.String

class Job(mongoengine.Document):
    latitude = mongoengine.FloatField(required=True)
    longitude = mongoengine.FloatField(required=True)

class JobSchema(ma.ModelSchema):
    class Meta:
         model = Job
         strict=True
