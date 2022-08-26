from twitter_scraper import scrape_tweets, create_dataframe_from_tweets_list
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__)

tweets = scrape_tweets("sengoku degens")
df = create_dataframe_from_tweets_list(tweets)

app.layout = html.Div(
    children=[
        html.H1(children="Twitter Dashboard NFT",),
        html.P(
            children="Analyze the tweets and sentiment of a NFT collection",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df.iloc[:, 0],
                        "y": df.iloc[:, 7],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Test graph"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)