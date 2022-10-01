from twitter_scraper import scrape_tweets, create_dataframe_from_tweets_list
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

df = pd.read_csv(r"C:\Code\twitter-dashboard-nft\src\test_df.csv")

df_most_tweets_by_user = df.groupby("Username")["ID"].count().nlargest(5)

fig_most_tweets_by_user = px.bar(df_most_tweets_by_user, x=df_most_tweets_by_user.index, y="ID", text_auto=True)

fig_geo = px.scatter_geo(df, lat="Latitude", lon="Longitude",
                     color="Country",
                     hover_name="Country", 
                     projection="natural earth")

app.layout = html.Div(className='row', children=[
    html.H1("NFT Trend"),
    html.P(children="Analyze the tweets and sentiment of a NFT collection",),
    html.Div(children=[
        dcc.Graph(id="most-tweets-by-user", style={'display': 'inline-block'}, figure=fig_most_tweets_by_user),
        dcc.Graph(id="geo-map", style={'display': 'inline-block'}, figure=fig_geo)
    ])
])



if __name__ == "__main__":
    app.run_server(debug=True)