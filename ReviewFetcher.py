import os
from dotenv import load_dotenv
import praw
import requests

class ReviewFetcher:
    def __init__(self):
        load_dotenv()

        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )

        self.serpapi_key = os.getenv('SERPAPI_KEY')

    def fetchReviews(self, product_name : str) -> list[str]:
        urls = self.fetchPosts(product_name)

        if urls:
            return self.fetchComments(urls)
        else:
            return []

    def fetchPosts(self, product_name : str) -> list[str]:
        try:
            # List to hold urls to be scraped
            urls = []

            # Parameters for GET request
            payload = {
                'engine': 'google',
                'q': f'site:www.reddit.com review {product_name}',
                'hl': 'en',
                'gl': 'us',
                'api_key': self.serpapi_key
            }

            # Sends GET request to SerpApi
            response = requests.get('https://serpapi.com/search', params=payload)

            # Checks for error
            response.raise_for_status()

            # Parses json response into dictionary
            api_data = response.json()

            # Looks at top 4 results from search and adds url to urls list
            for result in api_data['organic_results'][:4]:
                urls.append(result['link'])

            return urls
        
        except:
            return []

    def fetchComments(self, urls : list[str]) -> list[str]:
        # List to hold comments to be analyzed
        comments = []

        for url in urls:
            submission = self.reddit.submission(url=url) # Finds submission by url
            submission.comment_sort = 'top' # Sort comments by top
            submission.comments.replace_more(threshold=3, limit=3)
            submission_comments = submission.comments.list()[:3] # Gets top 3 comments from submission

            for comment in submission_comments[:3]: # Adds the comments to comments list
                comments.append(comment.body)

        return comments
