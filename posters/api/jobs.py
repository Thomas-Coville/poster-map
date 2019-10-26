from flask_restplus import Namespace, Resource, fields

from services import jobs

ns = Namespace('jobs')

# models

job = ns.model('Job', {
    'id': fields.Integer(readOnly=True, description='The Job\' unique identifier'),
})


@ns.route('')
class Jobs(Resource):
    @ns.doc('start_job')
    @ns.marshal_list_with(job)
    def post(self):
        '''Creates a new Job'''
        jobs.start_job()
        pass


@ns.route('/<id>')
@ns.param('id', 'The job identifier')
@ns.response(404, 'Job not found')
class Poster(Resource):
    @ns.doc('get_job')
    @ns.marshal_with(job)
    def get(self, id):
        '''Get a Job by ID'''
        pass
