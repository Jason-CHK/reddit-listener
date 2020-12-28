import argparse

from mech_market import MechMarketSubmission
from reddit import Reddit


def main(reddit_id: str,
         reddit_secret: str,
         discord_id: str,
         discord_secret: str):
    reddit = Reddit(reddit_id, reddit_secret)
    for s in reddit.subreddit_stream('mechmarket', skip_existing=False):
        sub = MechMarketSubmission(s)
        if sub.should_notify():
            print(sub)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Listen to reddit and notify with discord.')
    parser.add_argument('--reddit_id')
    parser.add_argument('--reddit_secret')
    parser.add_argument('--discord_id')
    parser.add_argument('--discord_secret')

    args = parser.parse_args()
    main(**vars(args))
