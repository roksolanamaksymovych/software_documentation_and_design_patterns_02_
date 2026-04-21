from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Owner(Base):
    __tablename__ = 'owners'
    ownerID = Column(Integer, primary_key=True)
    firstName = Column(String); lastName = Column(String); email = Column(String)
    apartments = relationship("Apartment", back_populates="owner")

class Apartment(Base):
    __tablename__ = 'apartments'
    apartmentID = Column(Integer, primary_key=True)
    ownerID = Column(Integer, ForeignKey('owners.ownerID'))
    address = Column(String); pricePerNight = Column(Float)
    description = Column(String); isAvailable = Column(Boolean)
    owner = relationship("Owner", back_populates="apartments")
    photos = relationship("Photo", back_populates="apartment")
    bookings = relationship("Booking", back_populates="apartment")
    reviews = relationship("Review", back_populates="apartment")

class Photo(Base):
    __tablename__ = 'photos'
    photoID = Column(Integer, primary_key=True)
    apartmentID = Column(Integer, ForeignKey('apartments.apartmentID'))
    imageURL = Column(String); caption = Column(String)
    apartment = relationship("Apartment", back_populates="photos")

class Booking(Base):
    __tablename__ = 'bookings'
    bookingID = Column(Integer, primary_key=True)
    apartmentID = Column(Integer, ForeignKey('apartments.apartmentID'))
    checkInDate = Column(Date); checkOutDate = Column(Date)
    status = Column(String); totalCost = Column(Float)
    apartment = relationship("Apartment", back_populates="bookings")

class Review(Base):
    __tablename__ = 'reviews'
    reviewID = Column(Integer, primary_key=True)
    apartmentID = Column(Integer, ForeignKey('apartments.apartmentID'))
    comment = Column(String); rating = Column(Integer); createdAt = Column(Date)
    apartment = relationship("Apartment", back_populates="reviews")