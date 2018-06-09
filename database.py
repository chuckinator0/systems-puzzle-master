import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
#Opened this host up to 0.0.0.0, but needed to change back for postgres to work.
host = 'db'
#Tried port 80 here, but it looks like this should be the postgres default port 5432.
#This was the source of a lot of self imposed misery.
#Do I need to expose this port in the docker-compose file?
#Added ports: - "5432:5432" to the docker-compose under the postgres image. No change.
#Tried expose: - "5432" in the yml file to expose postgres to other containers. No change.
#Try EXPOSE: 5432 in the dockerfile. No Change.
port = '5432'
engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db)) 

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
