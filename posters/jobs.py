from flask import Blueprint
from webargs.flaskparser import use_args
from models import JobSchema
import logging
from services import JobsService

bp = Blueprint('jobs', __name__)
logger = logging.getLogger()

# API
@bp.route('/jobs', methods=['POST'])
@use_args(JobSchema())
def create_job(args):        

    job = JobsService.create_job(args.latitude, args.longitude)

    return JobSchema().dump(job)

@bp.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):        
    job = JobsService.getJobById(job_id)
    return JobSchema().dump(job)