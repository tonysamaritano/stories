import os
import datetime

from sqlalchemy import Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine(os.environ.get("DATABASE_URL"),
                       connect_args={"check_same_thread": False}, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# class Simulation(Base):
#     __tablename__ = 'simulations'

#     id = Column(Integer, primary_key=True)
#     uuid = Column(String, unique=True)
#     created = Column(DateTime, default=datetime.datetime.utcnow)
#     type = Column(String)
#     owner = Column(String)

#     logs = relationship("Log", back_populates="simulation")
#     reports = relationship("Report", back_populates="simulation")

#     vbake_id = Column(Integer, ForeignKey("vbakes.id"))
#     vbake = relationship("VBake", uselist=False)

#     vpkg_id = Column(Integer, ForeignKey("vpkgs.id"))
#     vpkg = relationship("VPackage", uselist=False)

#     config_id = Column(Integer, ForeignKey("configs.id"))
#     config = relationship("Configuration", uselist=False)


# class Log(Base):
#     __tablename__ = 'logs'

#     id = Column(Integer, primary_key=True)
#     simulation_id = Column(Integer, ForeignKey("simulations.id"))
#     log = Column(String)
#     type = Column(String)

#     simulation = relationship("Simulation", back_populates="logs")


# class Report(Base):
#     __tablename__ = 'reports'

#     id = Column(Integer, primary_key=True)
#     simulation_id = Column(Integer, ForeignKey("simulations.id"))
#     report = Column(String)
#     type = Column(String)

#     simulation = relationship("Simulation", back_populates="reports")


# class VBake(Base):
#     __tablename__ = 'vbakes'

#     id = Column(Integer, primary_key=True)
#     owner = Column(String)
#     vbake = Column(String)


# class VPackage(Base):
#     __tablename__ = 'vpkgs'

#     id = Column(Integer, primary_key=True)
#     vpkg = Column(String)
#     owner = Column(String)


# class Configuration(Base):
#     __tablename__ = 'configs'

#     id = Column(Integer, primary_key=True)
#     config = Column(String)
#     owner = Column(String)

class Story(Base):
    __tablename__ = 'story'

    id = Column(Integer, primary_key=True)

    owner = Column(String)

    request_id = Column(Integer, ForeignKey("story_requests.id"))
    request = relationship("StoryRequest", uselist=False)

    title = Column(String, default=None)
    content = Column(String, default=None)
    img = Column(String, default=None)

    preview = Column(String, default=None)
    meta = Column(String, default=None)


class Pet(Base):
    __tablename__ = 'pet'

    id = Column(Integer, primary_key=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", uselist=False)

    name = Column(String)
    breed = Column(String)
    gender = Column(String)
    photo = Column(String, default=None)


class StoryRequest(Base):
    __tablename__ = 'story_requests'

    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pet.id"))
    pet = relationship("Pet", uselist=False)

    owner = Column(String)

    adj_0 = Column(String)
    adj_1 = Column(String)
    adj_2 = Column(String)

    backstory = Column(String, default=None)
    details = Column(String, default=None)

    status = Column(String, default="pending")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String, default="none")
    first_name = Column(String)
    last_name = Column(String)
    picture = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    disabled = Column(Boolean, default=False)
    tokens = Column(Integer)


Base.metadata.create_all(engine)
