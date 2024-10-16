from sqlalchemy import create_engine, Column, BigInteger, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from settings import DATABASE_URL
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    channel_id = Column(BigInteger)
    analytics_time = Column(String)
    timezone = Column(String, default='UTC')
    language = Column(String, default='en')

    __table_args__ = (Index('ix_users_telegram_id', 'telegram_id'),)

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def store_user_data(user_id: int, data: Dict[str, any]) -> None:
    try:
        session = Session()
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            user = User(telegram_id=user_id)
            session.add(user)
        
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        session.commit()
        logger.info(f"Stored data for user {user_id}")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error storing data for user {user_id}: {str(e)}")
    finally:
        Session.remove()

def get_user_data(user_id: int) -> Optional[Dict[str, any]]:
    try:
        session = Session()
        user = session.query(User).filter_by(telegram_id=user_id).first()
        
        if user:
            return {
                'channel': user.channel_id,
                'time': user.analytics_time,
                'timezone': user.timezone,
                'language': user.language
            }
        return None
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving data for user {user_id}: {str(e)}")
        return None
    finally:
        Session.remove()