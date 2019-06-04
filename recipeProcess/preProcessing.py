import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer('english')

def preProcessing(example):
    letters_only = re.sub('[^a-zA-Z]', ' ', example)
    lower_case = letters_only.lower()
    words = lower_case.split()
    words = [w for w in words if not w in stopwords.words('english')]
    words = [stemmer.stem(w) for w in words]
    words = [wordnet_lemmatizer.lemmatize(w) for w in words]
    return words
