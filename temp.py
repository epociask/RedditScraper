from config import *
import praw

reddit = praw.Reddit(client_id=clientId, client_secret=pk, user_agent=userAgent)


hot_posts = reddit.subreddit('Bitcoin').hot(limit=10)
for post in hot_posts:
    print(post.title)

import pandas as pd
posts = []
ml_subreddit = reddit.subreddit('Bitcoin')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

print(posts)
submissions = []

for post in posts['url']:
	print(post)

sub = reddit.submission(url = "https://www.reddit.com/r/Bitcoin/comments/f6708k/daily_discussion_february_19_2020/")

for comment in sub.comments:
	print(comment.body)