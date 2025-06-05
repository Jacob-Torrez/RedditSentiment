import ReviewFetcher

def main():
    fetcher = ReviewFetcher.ReviewFetcher()

    reviews = fetcher.fetchReviews('sony xm4')

    for review in reviews:
        print(review)

if __name__ == '__main__':
    main()
