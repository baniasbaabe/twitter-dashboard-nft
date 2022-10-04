import re
import string

import emoji
import nltk
import numpy as np

nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

stop_words = list(stopwords.words("english"))

sid_obj = SentimentIntensityAnalyzer()


def preprocess_tweet(text):
    text = text.lower()
    text = re.sub(
        r"(@[A-Za-z0-9]+)|(RT\s?@[A-Za-z0-9])", "", text
    )  # Remove Mentions and Retweet
    text = re.sub(r"https?:\/\/\S*", "", text)  # Remove links
    # Remove duplicated words
    words = text.split()
    text = " ".join(sorted(set(words), key=words.index))
    text = text.translate(
        str.maketrans("", "", string.punctuation + string.digits)
    )  # Remove digits and punctuation
    text = emoji.replace_emoji(text, "")
    tokens = word_tokenize(text)
    no_stops = [word for word in tokens if word not in stop_words]
    text = " ".join(no_stops)
    return text


def apply_sentiment(tweet):
    return sid_obj.polarity_scores(tweet).get("compound")


def bin_sentiment(sentiment):
    return (
        "Negative"
        if sentiment <= -0.05
        else "Positive"
        if sentiment >= 0.05
        else "Neutral"
    )


def preprocess_pipeline(df):
    df["Content_Preprocessed"] = df["Content"].apply(preprocess_tweet)

    df["Sentiment"] = df["Content_Preprocessed"].apply(apply_sentiment)

    df["Sentiment_String"] = df["Sentiment"].apply(bin_sentiment)
    
    return df
