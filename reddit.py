from hidden import *
import praw
import pandas as pd


def getSubredditData(subName):
    reddit = praw.Reddit(client_id=clientId, client_secret=pk, user_agent=userAgent)
    posts = []
    try:
        subreddit = reddit.subreddit(subName)

    except Exception as e:
        print("ERROR: ", e)
        return None

    for post in subreddit.new(limit=100):
        posts.append(
            [post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts, columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

    return posts
