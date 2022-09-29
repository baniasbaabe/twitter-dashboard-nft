from twitter_scraper import scrape_tweets, create_dataframe_from_tweets_list
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

# tweets = scrape_tweets("sengoku degens")
# df = create_dataframe_from_tweets_list(tweets)

df = pd.read_csv(r"C:\Code\twitter-dashboard-nft\src\test_df.csv")

fig = px.scatter(df, x="Retweet_Count", y="Like_Count", size_max=60)

fig_geo = px.scatter_geo(df, lat="Latitude", lon="Longitude",
#                      color="continent", # which column to use to set the color of markers
                     hover_name="Country", # column added to hover information
#                      size="Followers_Count", # size of markers
                    projection="natural earth")

app.layout = html.Div(className='row', children=[
    html.H1("NFT Trend"),
    html.P(children="Analyze the tweets and sentiment of a NFT collection",),
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
        dcc.Graph(id="graph2", style={'display': 'inline-block'}, figure=fig),
        dcc.Graph(id="graph3", style={'display': 'inline-block'}, figure=fig_geo)
    ])
])



if __name__ == "__main__":
    app.run_server(debug=True)