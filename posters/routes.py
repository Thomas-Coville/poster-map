from flask import Flask, jsonify, Blueprint
from webargs import fields
from webargs.flaskparser import use_args
from models import JobSchema
from services import JobsService
import tasks
import logging

bp = Blueprint('jobs', __name__)
logger = logging.getLogger()

# API
@bp.route('/jobs', methods=['POST'])
# @use_args(JobSchema())
def create_job():
    logger.info('FOOOO')
    tasks.say_hello.delay('thomas')
    pass
    # service = JobsService()

    # job = service.create_job( latitude=args["latitude"],
    #     longitude=args["longitude"])

    # schema = JobSchema()
    # return schema.dump(job)

