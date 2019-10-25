from flask_restplus import Namespace, Resource, fields

api = Namespace('jobs')

#models

job = api.model('Job', {
    'id': fields.Integer(readOnly=True, description='The Job\' unique identifier'),    
})


@api.route('')
class Jobs(Resource):
    @api.doc('start_job')
    @api.marshal_list_with(job)
    def post(self):
        '''Creates a new Job'''
        pass

@api.route('/<id>')
@api.param('id', 'The job identifier')
@api.response(404, 'Job not found')
class Poster(Resource):
    @api.doc('get_job')
    @api.marshal_with(job)
    def get(self, id):
        '''Get a Job by ID'''
        pass


