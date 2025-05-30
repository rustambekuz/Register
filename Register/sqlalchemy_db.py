from sqlalchemy import create_engine, Column, Integer, String, CheckConstraint
from sqlalchemy.orm import declarative_base, sessionmaker

dbs_url = 'postgresql+psycopg2://postgres:1234@localhost:5432/users'
engine = create_engine(dbs_url, echo=True)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True)
    address = Column(String(100), nullable=True)

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.id}, {self.first_name!r}, {self.last_name}),"
                f" {self.username!r}, {self.phone!r}, {self.email!r}, {self.address!r})")


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()











