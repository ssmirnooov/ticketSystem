from ma import ma
from models.Ticket import TicketModel
from models.Comment import CommentModel
from schemas.Comment import CommentSchema


class TicketSchema(ma.SQLAlchemyAutoSchema):
    comments = ma.Nested(CommentSchema, many=True)

    class Meta:
        model = TicketModel
        load_instance = True
        include_fk = True
