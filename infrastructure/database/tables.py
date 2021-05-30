from sqlalchemy import ARRAY, Column, MetaData, Table, Text
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()


TweetTable = Table(
    'tweet',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('text', Text, nullable=False),
    Column('tweeted_user_id', UUID(as_uuid=True), nullable=False),
    Column('liked_user_ids', ARRAY(UUID(as_uuid=True)), nullable=False),
    Column('retweeted_user_ids', ARRAY(UUID(as_uuid=True)), nullable=False),
)
