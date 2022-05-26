from flask import Flask, Blueprint, jsonify
from flask_restx import Api
from ma import ma
from db import db
from cache import cache

from resources.Ticket import Ticket, TicketList, ticket_ns, tickets_ns
from resources.Comment import Comment, CommentList, comment_ns, comments_ns
from marshmallow import ValidationError

app = Flask(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc', title='Ticket System')
app.register_blueprint(blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:user@db:5432/default_db'
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'redis'
app.config['CACHE_REDIS_PORT'] = '6379'
app.config['CACHE_REDIS_DB'] = '0'
app.config['CACHE_REDIS_URL'] = 'redis://redis:6379/0'
app.config['CACHE_DEFAULT_TIMEOUT'] = '500'


@app.before_first_request
def create_tables():
    db.create_all()


api.add_namespace(comment_ns)
api.add_namespace(comments_ns)
api.add_namespace(ticket_ns)
api.add_namespace(tickets_ns)

db.init_app(app)
ma.init_app(app)
cache.init_app(app)


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


comment_ns.add_resource(Comment, '/<int:id>')
comments_ns.add_resource(CommentList, '')
ticket_ns.add_resource(Ticket, '/<int:id>')
tickets_ns.add_resource(TicketList, '')





