"""
The SQLAlchemy models for creating the database tables.
The models are based on the Twitter API v2 Tweet object. 
It is an opnionated normalization of the Tweet object 
to make it easier to query the database.
"""


from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base
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

    tweet_type = Column(
        Integer,
        doc="""
        The type of the tweet 
        0: original, 
        1: quote tweet, 
        2: retweeted tweet, 
        3: reply, 
        4: quoted tweet + replied to tweet
        """,
    )

    retweet_count = Column(Integer, doc="The number of times the tweet was retweeted")
    reply_count = Column(Integer, doc="The number of times the tweet was replied to")
    like_count = Column(Integer, doc="The number of times the tweet was liked")
    quote_count = Column(Integer, doc="The number of times the tweet was quoted")
    impression_count = Column(Integer, doc="The number of times the tweet was viewed")
    edits_remaining = Column(Integer, doc="The number of times the tweet can be edited")
    is_edit_eligible = Column(Boolean, doc="Whether the tweet can be edited")
    editable_until = Column(
        DateTime, doc="The date and time when the tweet can no longer be edited"
    )

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
    location = Column(Text, nullable=True, doc="The location of the author")
    verified = Column(Boolean, doc="Whether the author is verified")
    protected = Column(Boolean, doc="Whether the author is protected")
    url = Column(Text, nullable=True, doc="The url of the author")
    profile_image_url = Column(
        Text, nullable=True, doc="The profile image url of the author"
    )
    followers_count = Column(Integer, doc="The number of followers of the author")
    following_count = Column(
        Integer, doc="The number of accounts the author is following"
    )
    tweet_count = Column(Integer, doc="The number of tweets of the author")
    listed_count = Column(Integer, doc="The number of lists the author is in")
