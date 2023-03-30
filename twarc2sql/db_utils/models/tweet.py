from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from . import Base
from sqlalchemy.orm import relationship


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(String(256), primary_key=True)
    created_at = Column(DateTime)
    text = Column(Text)
    possibly_sensitive = Column(Boolean)
    conversation_id = Column(Text)
    author_id = Column(String(256), ForeignKey("author.id"))
    source = Column(Text)
    reply_settings = Column(Text, nullable=True)
    lang = Column(Text, nullable=True)
    retweet_count = Column(Integer)
    like_count = Column(Integer)
    quote_count = Column(Integer)
    reply_count = Column(Integer)
    
    tweet_type = Column(Integer)

    author = relationship("Author", back_populates="tweets")


class Author(Base):

    __tablename__ = "author"

    id = Column(String(256), primary_key=True)
    name = Column(Text)
    username = Column(Text)
    created_at = Column(DateTime)
    description = Column(Text, nullable=True)
    

class HashTag(Base):
    __tablename__ = "hashtag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(Text)
    tweet_id = Column(String(256), ForeignKey("tweet.id"))
