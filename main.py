import SentimentModel
import ReviewFetcher

def main():
    model = SentimentModel.SentimentModel()
    fetch = ReviewFetcher.ReviewFetcher()

    model.loadModel()
    reviews = fetch.fetchReviews('INSERT PRODUCT HERE')
    ratings = model.predictSentiment(reviews)

    print(f'average: {sum(ratings) / len(ratings)}')



if __name__ == '__main__':
    main()
