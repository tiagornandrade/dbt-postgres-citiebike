import random
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Station(Base):
    __tablename__ = 'stations'

    station_id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    dockcount = Column(Integer)
    landmark = Column(String)
    installation_date = Column(DateTime)
    created_at = Column(DateTime)


class Status(Base):
    __tablename__ = 'status'

    station_id = Column(Integer, primary_key=True)
    bikes_available = Column(Integer)
    docks_available = Column(Integer)
    time = Column(DateTime)
    created_at = Column(DateTime)


class Trips(Base):
    __tablename__ = 'trips'

    trip_id = Column(Integer, primary_key=True)
    duration_sec = Column(Integer)
    start_date = Column(DateTime)
    start_station_name = Column(String)
    start_station_id = Column(Integer)
    end_date = Column(DateTime)
    end_station_name = Column(String)
    end_station_id = Column(Integer)
    bike_number = Column(Integer)
    zip_code = Column(String)
    subscriber_type = Column(String)
    created_at = Column(DateTime)


class FakerEvents:

    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.fake = Faker()

    def generate_fake_station(self):
        return {
            "station_id": random.randint(1, 1000),
            "name": self.fake.name(),
            "latitude": self.fake.latitude(),
            "longitude": self.fake.longitude(),
            "dockcount": random.randint(1, 1000),
            "landmark": self.fake.city(),
            "installation_date": self.fake.date_time_between(start_date="-30y", end_date="now"),
            "created_at": datetime.now(),
        }

    def generate_fake_status(self):
        return {
            "station_id": random.randint(1, 1000),
            "bikes_available": random.randint(1, 1000),
            "docks_available": random.randint(1, 1000),
            "time": self.fake.date_time_between(start_date="-30y", end_date="now"),
            "created_at": datetime.now(),
        }

    def generate_fake_trip(self):
        return {
            "trip_id": random.randint(1, 1000),
            "duration_sec": random.randint(1, 1000),
            "start_date": self.fake.date_time_between(start_date="-30y", end_date="now"),
            "start_station_name": self.fake.name(),
            "start_station_id": random.randint(1, 1000),
            "end_date": self.fake.date_time_between(start_date="-30y", end_date="now"),
            "end_station_name": self.fake.name(),
            "end_station_id": random.randint(1, 1000),
            "bike_number": random.randint(1, 1000),
            "zip_code": self.fake.zipcode(),
            "subscriber_type": self.fake.name(),
            "created_at": datetime.now(),
        }

    def generate_fake_data(self, sample_size, generate_function):
        fake_data = []
        for _ in range(sample_size):
            fake_data.append(generate_function())
        return fake_data

    def create_stations(self, x):
        fake_stations = self.generate_fake_data(x, self.generate_fake_station)
        with self.Session() as session:
            try:
                for fake_station in fake_stations:
                    print("Inserting station:", fake_station)
                    station = Station(**fake_station)
                    session.add(station)
                session.commit()
                print("Stations inserted successfully.")
            except Exception as e:
                print("Error inserting stations:", e)
                session.rollback()

    def create_status(self, x):
        fake_status = self.generate_fake_data(x, self.generate_fake_status)
        with self.Session() as session:
            for fake_stat in fake_status:
                status = Status(**fake_stat)
                session.add(status)
            session.commit()

    def create_trips(self, x):
        fake_trips = self.generate_fake_data(x, self.generate_fake_trip)
        with self.Session() as session:
            for fake_trip in fake_trips:
                trip = Trips(**fake_trip)
                session.add(trip)
            session.commit()

    def create_engine_and_session(db_uri):
        engine = create_engine(db_uri)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        return engine, Session