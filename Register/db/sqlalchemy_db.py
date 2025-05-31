from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from Register.handlers.config import DB_URL
from sqlalchemy import Column, Integer, String, BigInteger

engine = create_async_engine(DB_URL, echo=True)


async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True)
    address = Column(String(100), nullable=True)

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.id}, {self.first_name!r}, {self.last_name}),"
                f" {self.username!r}, {self.phone!r}, {self.email!r}, {self.address!r})")











