import RedditFetcher

def main():
    rapi = RedditFetcher.RedditFetcher()
    for comment in rapi.fetchComments('"Sony WH-1000XM4" review'):
        print(comment + '\n')

if __name__ == '__main__':
    main()
