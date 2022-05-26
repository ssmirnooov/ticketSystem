from ma import ma
from models.Ticket import TicketModel
from models.Comment import CommentModel


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CommentModel
        load_instance = True
        load_only = ('ticket', )
        include_fk = True

