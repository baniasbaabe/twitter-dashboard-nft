from twitter_scraper import scrape_tweets, create_dataframe_from_tweets_list
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__)

# tweets = scrape_tweets("sengoku degens")
# df = create_dataframe_from_tweets_list(tweets)

df = pd.read_csv(r"C:\Code\twitter-dashboard-nft\src\test_df.csv")

# app.layout = html.Div(
#     children=[
#         html.H1(children="Twitter Dashboard NFT",),
#         html.P(
#             children="Analyze the tweets and sentiment of a NFT collection",
#         ),
#         dcc.Graph(
#             figure={
#                 "data": [
#                     {
#                         "x": df.loc[:, "Date"],
#                         "y": df.loc[:, "Followers_Count"],
#                         "type": "lines",
#                     },
#                 ],
#                 "layout": {"title": "Test graph"},
#             },
#         ),
#     ]
# )

app.layout = html.Div(className='row', children=[
    html.H1("Tips database analysis (First dashboard)"),
    dcc.Dropdown(),
    html.Div(children=[
        dcc.Graph(id="graph1", style={'display': 'inline-block'}, figure={
                "data": [
                    {
                        "x": df.loc[:, "Date"],
                        "y": df.loc[:, "Followers_Count"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Test graph"},
            },),
        dcc.Graph(id="graph2", style={'display': 'inline-block'}, figure={
                "data": [
                    {
                        "x": df.loc[:, "Retweet_Count"],
                        "y": df.loc[:, "Followers_Count"],
                        "type": "scatter",
                    },
                ],
                "layout": {"title": "Test graph"},
            },)
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)