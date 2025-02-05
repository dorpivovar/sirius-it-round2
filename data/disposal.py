# import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin


class Disposal(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'disposal'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    images = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    website = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    maps_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)