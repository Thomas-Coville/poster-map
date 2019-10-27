from flask import Flask, jsonify, Blueprint
from webargs import fields
from webargs.flaskparser import use_args
from models import JobSchema
import tasks
import logging

bp = Blueprint('jobs', __name__)
logger = logging.getLogger()

# API
@bp.route('/jobs', methods=['POST'])
# @use_args(JobSchema())
def create_job():    
    logger.info(f'task name is {tasks.say_hello.name}')

    tasks.say_hello.delay('thomas')
    return "OK"

