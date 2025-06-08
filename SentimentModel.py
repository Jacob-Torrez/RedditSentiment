from datasets import load_dataset
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import make_pipeline
from TextPreprocessor import preprocessText
from joblib import dump, load

class SentimentModel:
    def __init__(self):
        self.tfidf_model = make_pipeline(TfidfVectorizer(), MultinomialNB())

    def saveModel(self):
        dump(self.tfidf_model, 'models/model.pkl')

    def loadModel(self):
        self.tfidf_model = load('models/model.pkl')

    def trainModel(self):
        dataset = load_dataset("amazon_polarity")
        x_train = [preprocessText(text) for text in dataset['train']['content']]
        y_train = dataset['train']['label']

        self.tfidf_model.fit(x_train, y_train)

        x_test = [preprocessText(text) for text in dataset['test']['content']]
        y_test = dataset['test']['label']

        y_predict = self.tfidf_model.predict(x_test)

        print(f"f1: {f1_score(y_test, y_predict, average='weighted'):.4f}")
        print(f'accuracy: {accuracy_score(y_test, y_predict):.4f}')
        

    def predictSentiment(self, corpus : list[str]):
        x_predict = [preprocessText(text) for text in corpus]
        y_predict = self.tfidf_model.predict(x_predict)
        return y_predict