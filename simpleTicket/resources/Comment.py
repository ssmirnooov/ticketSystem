from flask import request
from flask_restx import Resource, fields, Namespace
from models.Comment import CommentModel
from schemas.Comment import CommentSchema
from cache import cache

COMMENT_NOT_FOUND = 'Comment not found.'

comment_ns = Namespace('comment', description='Comment related operations')
comments_ns = Namespace('comments', description='Comments related operations')

comment_schema = CommentSchema()
comments_list_schema = CommentSchema(many=True)

comment = comment_ns.model('Comment', {
    'email': fields.String('commenter email'),
    'text': fields.String('comment text'),
    'ticket_id': fields.Integer
})


class Comment(Resource):
    @cache.cached(timeout=30, query_string=True)
    def get(self):
        comment_data = CommentModel.find_by_id(id)
        if comment_data:
            return comment_schema.dump(comment_data)
        return {'message': COMMENT_NOT_FOUND}, 404


class CommentList(Resource):
    @cache.cached(timeout=30, query_string=True)
    @comments_ns.doc('Get all comments')
    def get(self):
        return  comments_list_schema.dump(CommentModel.find_all()), 200

    @comments_ns.expect(comment)
    @comments_ns.doc('Create a comment')
    def post(self):
        comment_json = request.get_json()
        comment_data = comment_schema.load(comment_json)
        comment_data.save_to_db()

        return comment_schema.dump(comment_data), 201
