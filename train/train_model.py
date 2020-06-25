import pickle
import re
import sys

import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from tqdm import tqdm

from config import Config

Config.MODELS_PATH.mkdir(parents=True, exist_ok=True)
# Config.METRICS_FILE_PATH.mkdir(parent=True, exist_ok=True)

REPLACE_NO_SPACE = re.compile("[.;:!?,\"()\[\]]")
tqdm.pandas()
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

stop_words = ['the', 'so', 'a', 'an', 'on', 'in', 'at', 'of', 'for',
              'are', 'is', "it's", 'be', 'or', 'any', 'and', 'like',
              'that', 'this', 'they', 'them', 'there', "there's", 'with', 'just', 'but', 'only', 'one', 'other', 'mean',
              'i', "i'm", 'he', 'she', 'it', 'we', 'you', 'our', 'us', 'my',
              'ok', 'okay', 'yeah', 'well', 'with']


def clean_text(review):
    review = REPLACE_NO_SPACE.sub("", review.lower())
    return review


def remove_stop_words(review):
    removed_stop_words = ' '.join([word for word in review.split() if word not in stop_words])
    return removed_stop_words


def get_stemmed_text(review):
    stemmed_reviews = ' '.join([stemmer.stem(word) for word in review.split()])
    return stemmed_reviews


def get_lemmatized_text(review):
    lemmatized_text = ' '.join([lemmatizer.lemmatize(word) for word in review.split()])
    return lemmatized_text


def setup_data(df):
    df['sentence'] = df['sentence'].astype(str).progress_apply(clean_text)
    df['sentence'] = df['sentence'].astype(str).progress_apply(remove_stop_words)
    # df['sentence'] = df['sentence'].astype(str).progress_apply(is_english_check)
    # df['sentence'] = df['sentence'].astype(str).progress_apply(get_stemmed_text)
    # df['sentence'] = df['sentence'].astype(str).progress_apply(get_lemmatized_text)
    df = df.dropna()
    return df


def save_as_pickled_object(obj, filepath):
    """
    This is a defensive way to write pickle.write, allowing for very large files on all platforms
    """
    max_bytes = 2 ** 31 - 1
    bytes_out = pickle.dumps(obj)
    n_bytes = sys.getsizeof(bytes_out)
    with open(filepath, 'wb') as f_out:
        for idx in range(0, n_bytes, max_bytes):
            f_out.write(bytes_out[idx:idx + max_bytes])


def train_tfidf_model(train_features_original,  train_labels, model_save_path):
    train_features = setup_data(train_features_original.copy()).dropna()

    X_train = train_features['sentence']
    y_train = train_labels.astype(int)

    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', LogisticRegression(C=1))])

    model.fit(X_train, y_train)
    pickle.dump(model, open(model_save_path, 'wb'))
    # save_as_pickled_object(model, model_save_path)



if __name__ == '__main__':
    train_features_df = pd.read_csv(str(Config.FEATURE_PATH / 'train_features.csv'))
    train_labels_df = pd.read_csv(str(Config.FEATURE_PATH / 'train_labels.csv'))
    train_features_df.columns = ['sentence']
    model_path = str(Config.MODELS_PATH / 'tfidf_model.pickle')
    metrics_path = str(Config.METRICS_FILE_PATH)

    train_tfidf_model(train_features_df, train_labels_df, model_path)

