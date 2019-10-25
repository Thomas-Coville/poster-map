from flask_restplus import Namespace, Resource, fields

api = Namespace('posters')

#models

poster = api.model('Poster', {
    'id': fields.Integer(readOnly=True, description='The poster unique identifier'),    
})


@api.route('')
class Posters(Resource):
    @api.doc('create_poster')
    @api.marshal_list_with(poster)
    def post(self):
        '''Creates a new Poster'''
        pass

@api.route('/<id>')
@api.param('id', 'The poster identifier')
@api.response(404, 'Poster not found')
class Poster(Resource):
    @api.doc('get_poster')
    @api.marshal_with(poster)
    def get(self, id):
        '''Get a Poster by ID'''
        pass


