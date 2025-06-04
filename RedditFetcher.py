import praw
import os
from dotenv import load_dotenv

class RedditFetcher:
    def __init__(self):
        load_dotenv()

        self.reddit = praw.Reddit(
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET'),
            user_agent=os.getenv('USER_AGENT')
        )

    def fetchComments(self, product_name : str):
        # Searching all subreddits
        all = self.reddit.subreddit('all')

        # List to hold comments to be analyzed
        comments = []

        # Go through the top 3 posts in the last year that have product name in the post
        for submission in all.search(query=product_name, sort='top', time_filter='year', limit=3):
            print(submission.url)
            submission.comment_sort = 'top' # Sort comments by top
            submission.comments.replace_more(limit=3)
            top_comments = submission.comments.list() # Convert CommentForest to list

            # Add top 3 comments to our comments list
            for comment in top_comments[:3]: 
                comments.append(comment.body)

        return comments
