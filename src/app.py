from multiprocessing.resource_sharer import stop
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import re
import string
import nltk
import emoji
import plotly.graph_objects as go
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = dash.Dash(__name__)

df = pd.read_csv(r"C:\Code\twitter-dashboard-nft\src\test_df.csv")

stop_words = list(stopwords.words("english"))

sid_obj = SentimentIntensityAnalyzer()

def preprocess_tweet(text):
    text = text.lower()
    text = re.sub(r"(@[A-Za-z0-9]+)|(RT\s?@[A-Za-z0-9])", "", text) # Remove Mentions and Retweet
    text = re.sub(r"https?:\/\/\S*", "", text) # Remove links
    # Remove duplicated words
    words = text.split()
    text = " ".join(sorted(set(words), key=words.index)) 
    text = text.translate(str.maketrans('', '', string.punctuation + string.digits)) # Remove digits and punctuation
    text = emoji.replace_emoji(text, "")
    tokens = word_tokenize(text)
    no_stops = [word for word in tokens if word not in stop_words]
    text = " ".join(no_stops)
    return text

def apply_sentiment(tweet):
    return sid_obj.polarity_scores(tweet).get("compound")

def bin_sentiment(sentiment):
    return "Negative" if sentiment < 0.5 else "Positive"

df["Content_Preprocessed"] = df["Content"].apply(preprocess_tweet)

df["Sentiment"] = df["Content_Preprocessed"].apply(apply_sentiment)

df["Sentiment_String"] = df["Sentiment"].apply(bin_sentiment)

df_most_tweets_by_user = df.groupby("Username")["ID"].count().nlargest(5)

series_most_frequent_words = pd.Series(' '.join(df['Content_Preprocessed']).lower().split()).value_counts()[:20].to_frame("Count")

df_sentiment = df.groupby("Sentiment_String").size().to_frame("Count")

fig_most_tweets_by_user = px.bar(df_most_tweets_by_user, x=df_most_tweets_by_user.index, y="ID", text_auto=True)

fig_geo = px.scatter_geo(df, lat="Latitude", lon="Longitude",
                     color="Country",
                     hover_name="Country", 
                     projection="natural earth")

fig_most_frequent_words = px.bar(series_most_frequent_words, x = series_most_frequent_words.index, y = "Count", text_auto=True)

fig_sentiment = px.bar(df_sentiment, x = df_sentiment.index, y = "Count", text_auto=True)


print(df["Sentiment"].head())

app.layout = html.Div(className='row', children=[
    html.H1("NFT Trend"),
    html.P(children="Analyze the tweets and sentiment of a NFT collection",),
    html.Div(children=[
        dcc.Graph(id="most-tweets-by-user", style={'display': 'inline-block'}, figure=fig_most_tweets_by_user),
        dcc.Graph(id="geo-map", style={'display': 'inline-block'}, figure=fig_geo)
    ]),
    html.Div(children=[
        dcc.Graph(id="mos", style={'display': 'inline-block'}, figure=fig_most_frequent_words),
        dcc.Graph(id="most-twee-usser", style={'display': 'inline-block'}, figure=fig_sentiment),   
    ])
    
])



if __name__ == "__main__":
    app.run_server(debug=True)