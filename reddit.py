from typing import Iterator

import praw
from praw.reddit import Submission

USER_AGENT = 'reddit listener script by u/wrn2x'


class Reddit(object):
    def __init__(self, client_id: str, client_secret: str, read_only: bool = True):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=USER_AGENT
        )
        self.reddit.read_only = read_only

    def subreddit_stream(self, subreddit, skip_existing: bool = False) -> Iterator[Submission]:
        sr = self.reddit.subreddit(subreddit)
        for s in sr.stream.submissions(skip_existing=skip_existing):
            yield self.reddit.submission(s)


class RedditSubmission(object):
    def __init__(self, sub: Submission):
        self.title = sub.title
        self.flair = sub.link_flair_text
        self.text = sub.selftext
        self.link = sub.permalink

    def should_notify(self) -> bool:
        """ Hints if the current submission should be notified. Override this. """
        return True

    def __str__(self) -> str:
        """ String representation of the submission that will be used for notification. Override this. """
        return f'title: {self.title}' \
               f'\n  link: https://www.reddit.com{self.link}'
