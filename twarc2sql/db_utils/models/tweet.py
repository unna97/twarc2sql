"""
The SQLAlchemy models for creating the database tables.
The models are based on the Twitter API v2 Tweet object. 
It is an opnionated normalization of the Tweet object 
to make it easier to query the database.
"""


from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(
        String(256),
        primary_key=True,
        nullable=False,
        unique=True,
        doc="The unique identifier of the tweet",
    )
    created_at = Column(DateTime, doc="The date and time when the tweet was created")
    text = Column(Text, doc="The text of the tweet")
    possibly_sensitive = Column(Boolean, doc="Whether the tweet is possibly sensitive")
    conversation_id = Column(Text, doc="The conversation id of the tweet")
    author_id = Column(
        String(256),
        ForeignKey("author.id"),
        nullable=False,
        doc="The author of the tweet",
    )
    # TODO: it's a Literal, find the complete list of possible values
    reply_settings = Column(Text, nullable=True, doc="The reply settings of the tweet")
    lang = Column(Text, nullable=True, doc="The language of the tweet")
    # TODO: Add FOREIGN KEY constraint
    in_reply_to_user_id = Column(
        String(256),
        nullable=True,
        doc="The user id of the user the tweet is replying to",
    )
    tweet_type = Column(Integer)

    author = relationship("Author", back_populates="tweets")


class Author(Base):
    __tablename__ = "author"

    id = Column(
        String(256),
        primary_key=True,
        nullable=False,
        unique=True,
        doc="The unique identifier of the author",
    )
    name = Column(Text, doc="The name of the author")
    username = Column(Text, doc="The username of the author")
    created_at = Column(DateTime, doc="The date and time when the author was created")
    description = Column(Text, nullable=True, doc="The description of the author")
