from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

#Import func so that we can set a server side timestamp.
from sqlalchemy.sql import func



class Items(Base):
    """
    Items table
    """
    __tablename__ = 'items'
    
##    #Try adding query here so flaskapp knows what to do at /success
##    #This didn't work because database.py is supposed to have the query setup for declarative.
##    query = db_session.query_property()
    
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    #Won't setting quantity=Column(Integer) give an error if the user doesn't unput and integer?
    quantity = Column(Integer)
    description = Column(String(256))
    '''
    DateTime may be causing the 504 error because the timestamp needs to be
    calculated by the server instead of the app. Try importing func and setting default to
    server_default = func.now()
    '''
    date_added = Column(DateTime(),server_default=func.now())

    #The code for init and repr is missing, so that might be why the table entries were empty.
    #This was it. Putting this in allowed query to work as intended. Challenge complete!
    def __init__(self,name,quantity,description,date_added):
        self.name = name
        self.quantity = quantity
        self.description = description
        self.date_added = date_added

    def __repr__(self):
        return '{} {} {} {} {}' .format(self.id, self.name, self.quantity, self.description, self.date_added)

    
