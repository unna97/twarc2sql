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
    "user_object": [
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
        "entities",
        "pinned_tweet_id",
        "public_metrics",
    ],
    "error_info_object": [
        "value",
        "detail",
        "title",
        "resource_type",
        "parameter",
        "resource_id",
        "type",
    ],
    "media_object": [
        "media_key",
        "type",
        "url",
        "duration_ms",
        "height",
        "preview_image_url",
        "public_metrics",
        "width",
        "alt_text",
        "variants",
    ],
    "places_object": [
        "full_name",
        "id",
        "contained_within",  # optional
        "name",
        "geo",
        "country_code",
        "country",
        "place_type",
    ],
    "polls_object": [
        "id",
        "options",
        "duration_minutes",
        "end_datetime",
        "voting_status",
    ],
    "list_object": [
        "id",
        "name",
        "created_at",
        "description",
        "follower_count",
        "member_count",
        "private",
        "owner_id",
    ],
}

# TODO: Use this to assign names for the tables
# TODO: Use this to prioritize the order of the tables when creating the database
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
        # "pinned_tweet_id",
        # Expanded columns
        "followers_count",
        "following_count",
        "tweet_count",
        "listed_count",
    ],
    "retweeted_tweet_mapping": [
        "tweet_id",
        "id",
    ],
    "quoted_tweet_mapping": ["tweet_id", "id"],
    "replied_to_tweet_mapping": [
        "id",
        "tweet_id",
        "in_reply_to_user_id",
    ],
}
