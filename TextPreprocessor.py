import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

slang_dict = {
    'idk': 'i don\'t know',
    'imo': 'in my opinion',
    'imho': 'in my humble opinion',
    'afaik': 'as far as i know',
    'fwiw': 'for what it\'s worth',
    'btw': 'by the way',
    'tbh': 'to be honest',
    'ik': 'i know',
    'ikr': 'i know right',
    'omw': 'on my way',
    'np': 'no problem',
    'b/c': 'because',
    'bc': 'because',
    'tho': 'though',
    'w/o': 'without',
    'w': 'with',
    'atm': 'at the moment',
    'ppl': 'people',
    'obv': 'obviously',
    'prob': 'probably',
    'def': 'definitely',
    'rly': 'really',
    'smth': 'something',
    'u': 'you',
    'ur': 'your',
    'vs': 'versus'
}

def expandSlang(text: str) -> str:
    words = text.split()
    expanded = [slang_dict.get(word, word) for word in words]
    return ' '.join(expanded)

def preprocessText(text: str) -> str:
    # Lowercase the text
    text = text.lower()

    # Expand slang abbreviations
    text = expandSlang(text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)

    # Remove non-letter characters
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return ' '.join(tokens)
