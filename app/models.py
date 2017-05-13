from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    email = Column(String(120), unique=True)
    password_hash = Column(String(120))
    last_name = Column(String(50))
    session_id = Column(String(120))
    telegram_id = Column(String(120))
    posts = relationship('Post', backref='author')

    def __init__(self, first_name, email, password_hash,
                 last_name=None):
        self.first_name = first_name
        self.email = email
        self.password_hash = password_hash
        self.last_name = last_name

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.email)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(240))
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    approve_voices = Column(Integer)
    decline_voices = Column(Integer)
    isActive = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, title=None, description=None, created_at=None, updated_at=None,
                 approve_voices=None, decline_voices=None, isActive=None, user_id=None):
        self.title = title
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.approve_voices = approve_voices
        self.decline_voices = decline_voices
        self.isActive = isActive
        self.user_id = user_id

    def __repr__(self):
        return '<Post {}>'.format(self.title)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    User.__table__.update()


