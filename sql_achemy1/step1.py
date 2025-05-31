from sqlalchemy import (create_engine, Column,
                        Integer, String, Text,
                        ForeignKey)

from sqlalchemy.orm import declarative_base, relationship, sessionmaker

pg_url="postgresql+psycopg2://postgres:1234@localhost/log"

engine = create_engine(pg_url, echo=True)


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    posts = relationship('Post', back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.name!r})'


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='posts')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.title!r})'

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# user1 = User(name='Hamza')
# session.add(user1)
# session.commit()
# post1 = Post(title='My first day 20', content='My first day content 20', user_id=user1.id)
# post2 = Post(title='My first day 21', content='My first day content 21', user_id=user1.id)
#
# session.add_all([post1, post2])
# session.commit()



