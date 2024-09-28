from .extensions import db
from flask_login import UserMixin  # Import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class Car(db.Model):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String(20), nullable=False)

class Host(db.Model):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    driving_licence = Column(String(20), nullable=False)
    id_card = Column(String(20), nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id'))
    car = relationship('Car', backref='hosts')

class Guest(db.Model, UserMixin):
    __tablename__ = 'guests'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    driving_licence = Column(String(20), nullable=False)
    id_card = Column(String(20), nullable=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False