from ast import arg
import re
import string

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output, State

from src.preprocess import preprocess_pipeline
from twitter_scraper import create_dataframe_from_tweets_list, scrape_tweets

app = dash.Dash(__name__)
app.title = "NFT Tracking Dashboard"
app._favicon = ("favicon.png")

app.layout = html.Div(
    className="row",
    children=[
        html.H1("NFT Trend", style={"text-align": "center"}),
        html.P(
            children="Analyze the tweets and sentiment of a NFT collection",
            style={"text-align": "center"},
        ),
        html.Br(),
        html.P(
            children="When trading with Non-Fungible-Tokens (NFT) one important aspect to stay updated on Twitter. On Twitter, NFT-influencer can share their opinion and maybe influence a NFT collection. E.g. a big influencer (and CEO of DeGods) named Frank can talk in a positive way about a NFT collection and consequently increasing the floor price.",
            style={"text-align": "center"},
        ),
        html.Br(),
        html.P(
            children="With this dashboard you have a quick overview over the collection XYZ to gain insights and use it as a decision support when trading with NFTs",
            style={"display": "block", "margin-right": "auto", "margin-left": "auto"},
        ),
        html.P(
            children="Type in a NFT collection and wait for the results*",
            style={"display": "block", "margin-right": "auto", "margin-left": "auto"},
        ),
        dcc.Input(
            id="input-handle",
            type="text",
            placeholder="NFT Collection",
            value="degods",
            style={"text-align": "center"},
        ),
        dcc.Input(
            id="input-number",
            type="text",
            placeholder="No. of Tweets",
            value="100",
            style={"text-align": "center"},
        ),
        html.Button(id="hit-button", children="submit", style={"text-align": "center"}),
        dcc.Loading(
            id="loading-1",
            type="default",
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id="most-tweets-by-user",
                            style={"display": "inline-block"},
                            figure={},
                        ),
                        dcc.Graph(
                            id="geo-map", style={"display": "inline-block"}, figure={}
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id="most-frequent-words",
                            style={"display": "inline-block"},
                            figure={},
                        ),
                        dcc.Graph(
                            id="sentiment",
                            style={"display": "inline-block"},
                            figure={},
                        ),
                    ]
                ),
                html.P(
                    children="*Since snscrape is used as the Twitter Scraper, it could be a bit time consuming for scraping the tweets.",
                    style={"text-align": "left"},
                ),
            ],
        ),
    ],
)


@app.callback(
    Output(component_id="most-tweets-by-user", component_property="figure"),
    Output(component_id="geo-map", component_property="figure"),
    Output(component_id="most-frequent-words", component_property="figure"),
    Output(component_id="sentiment", component_property="figure"),
    Input(component_id="hit-button", component_property="n_clicks"),
    State(component_id="input-handle", component_property="value"),
    State(component_id="input-number", component_property="value"),
)
def display_value(nclicks, count_handle, no_tweets):

    tweets = scrape_tweets(count_handle, n=int(no_tweets))
    print(nclicks, count_handle, no_tweets)
    df = create_dataframe_from_tweets_list(tweets)

    df = preprocess_pipeline(df)

    df_most_tweets_by_user = df.groupby("Username")["ID"].count().nlargest(5)

    series_most_frequent_words = (
        pd.Series(" ".join(df["Content_Preprocessed"]).lower().split())
        .value_counts()[:20]
        .to_frame("Count")
    )

    df_sentiment = df.groupby("Sentiment_String").size().to_frame("Count")

    fig_most_tweets_by_user = px.bar(
        df_most_tweets_by_user, x=df_most_tweets_by_user.index, y="ID", text_auto=True
    )

    fig_geo = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Country",
        hover_name="Country",
        projection="natural earth",
    )

    fig_most_frequent_words = px.bar(
        series_most_frequent_words,
        x=series_most_frequent_words.index,
        y="Count",
        text_auto=True,
    )

    fig_sentiment = px.bar(
        df_sentiment, x=df_sentiment.index, y="Count", text_auto=True
    )

    return fig_most_tweets_by_user, fig_geo, fig_most_frequent_words, fig_sentiment


if __name__ == "__main__":
    app.run_server(debug=True)
