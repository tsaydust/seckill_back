from . import Base
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
import random
import string
from sqlalchemy_serializer import SerializerMixin
from settings import WORKER_ID, DATACENTER_ID
from utils.snowflake.snowflake import Snowflake

snowflake = Snowflake(DATACENTER_ID, WORKER_ID)


def generate_username():
    user_id = "".join(random.sample(string.digits, 6))
    return "用户" + user_id


def generate_snowflake_id():
    new_id = snowflake.get_id()
    return new_id


class User(Base, SerializerMixin):
    __tablename__ = 'user'
    # serialize_only = ('id', 'mobile')
    # serialize_rules = ('-password', "-addresses")
    serialize_only = ('id', 'mobile', 'username', 'avatar', 'is_active', 'is_staff')
    id = Column(BigInteger, primary_key=True, default=generate_snowflake_id)
    mobile = Column(String(20), unique=True, index=True)
    username = Column(String(20), default=generate_username)
    password = Column(String(300), nullable=True)
    avatar = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
