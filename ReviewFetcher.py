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

        for url in urls:
            print(url)

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
                'q': f'site:www.reddit.com "your experience" OR "worth it" OR "thoughts?" OR "would you" {product_name}',
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

            wanted_keywords = {"feedback", "experience", "thoughts", "worth", "opinion", "owners", "review"}
            unwanted_keywords = {"vs", "comparison", "my"}

            # Looks at top 4 results from search and adds url to urls list
            count = 0
            for result in api_data['organic_results']:
                if (count >= 3):
                    break

                title = result['title'].lower()
                title_words = set(title.split())

                if (title_words & wanted_keywords and not title_words & set(unwanted_keywords)):
                    urls.append(result['link'])
                    count += 1

            return urls
        
        except:
            return []

    def fetchComments(self, urls : list[str]) -> list[str]:
        # List to hold comments to be analyzed
        comments = []

        for url in urls:
            submission = self.reddit.submission(url=url) # Finds submission by url
            submission.comment_sort = 'top' # Sort comments by top
            submission.comments.replace_more(limit=0)

            count = 0
            for comment in submission.comments.list(): # Adds the comments to comments list
                if (count >= 3):
                    break
                if (
                    comment.author
                    and comment.body.lower().strip() != '[removed]'
                    and comment.author.name.lower() != 'automoderator'
                ):
                    comments.append(comment.body)
                    count += 1

        return comments
