from flask import request
from flask_restx import Resource, fields, Namespace

from models.Ticket import TicketModel
from schemas.Ticket import TicketSchema
from cache import cache

TICKET_NOT_FOUND = 'Ticket not found.'
TICKET_ALREADY_EXISTS = 'Ticket %s already exists.'

ticket_ns = Namespace('ticket', description='Ticket related operations')
tickets_ns = Namespace('tickets', description='Tickets related operations')

ticket_schema = TicketSchema()
ticket_list_schema = TicketSchema(many=True)

ticket = tickets_ns.model('Ticket', {
    'topic': fields.String('Name of the Ticket'),
    'text': fields.String('Some texts'),
    'email': fields.String('s@s.ru')
})


class Ticket(Resource):
    @cache.cached(timeout=30, query_string=True)
    def get(self, id):
        ticket_data = TicketModel.find_by_id(id)
        if ticket_data:
            return ticket_schema.dump(ticket_data)
        return {'message': TICKET_NOT_FOUND}, 404

    def delete(self, id):
        ticket_data = TicketModel.find_by_id(id)
        if ticket_data:
            ticket_data.delete_from_db()
            return {'message': 'Ticket Deleted'}, 200
        return {'message': TICKET_NOT_FOUND}, 404

    @tickets_ns.expect(ticket)
    def put(self, id):
        data = request.get_json()
        ticket_data = TicketModel.find_by_id(id)
        if ticket_data:
            ticket_data.status = data['status']
            ticket_data.save_to_db()
            return ticket_schema.dump(ticket_data), 200
        return {'message': TICKET_NOT_FOUND}, 404


class TicketList(Resource):
    @cache.cached(timeout=30, query_string=True)
    @tickets_ns.doc('Get all the Tickets')
    def get(self):
        return ticket_list_schema.dump(TicketModel.find_all()), 200

    @tickets_ns.expect(ticket)
    @tickets_ns.doc('Create ticket')
    def post(self):
        ticket_json = request.get_json()
        topic = ticket_json['topic']
        if TicketModel.find_by_topic(topic):
            return {'message': TICKET_ALREADY_EXISTS % topic}, 404

        ticket_data = ticket_schema.load(ticket_json)
        ticket_data.save_to_db()

        return ticket_schema.dump(ticket_data), 201
