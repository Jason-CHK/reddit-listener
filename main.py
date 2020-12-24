import sys

from mech_market import MechMarketSubmission
from reddit import Reddit


def main(reddit_client_id: str,
         reddit_client_secret: str):
    reddit = Reddit(reddit_client_id, reddit_client_secret)
    for s in reddit.subreddit_stream('mechmarket', skip_existing=False):
        sub = MechMarketSubmission(s)
        if sub.should_notify():
            print(sub)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python main.py <client id> <client secret>')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
