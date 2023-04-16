"""Module for file utilities for twarc2sql."""
objects = {
    "tweets_object": [],
    "users_object": [],
    "media_object": [],
    "places_object": [],
    "polls_object": [],
    "meta_object": [],
    "error_info_object": [],
}

object_columns = {
    "tweet_object": [
        "edit_history_tweet_ids",
        "text",
        "edit_controls",
        "conversation_id",
        "lang",
        "entities",
        "possibly_sensitive",
        "author_id",
        "reply_settings",
        "id",
        "created_at",
        "public_metrics",
        "context_annotations",
        "referenced_tweets",
        "attachments",
        "in_reply_to_user_id",
        "geo",
    ],
    "user_object": [],
}

table_columns = {
    "tweet": [
        # copy the tweet object columns as is
        "text",
        "conversation_id",
        "lang",
        "possibly_sensitive",
        "author_id",
        "reply_settings",
        "id",
        "created_at",
        "in_reply_to_user_id",
        # Expanded columns
        "retweet_count",
        "reply_count",
        "like_count",
        "quote_count",
        "impression_count",
        "edits_remaining",
        "is_edit_eligible",
        "editable_until",
        # From processed columns
        "tweet_type",
    ],
    "author": [
        # copy the user object columns as is
        "created_at",
        "description",
        "id",
        "location",
        "name",
        "profile_image_url",
        "protected",
        "url",
        "username",
        "verified",
        # Expanded columns
        "followers_count",
        "following_count",
        "tweet_count",
        "listed_count",
    ],
}
