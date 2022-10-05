import pandas as pd
import snscrape.modules.twitter as sntwitter
HEADER = [
    "ID",
    "Date",
    "Source_Label",
    "Content",
    "URL",
    "User_ID",
    "Username",
    "Followers_Count",
    "Reply_Count",
    "Retweet_Count",
    "Like_Count",
    "Quote_Count",
    "Lang",
    "Longitude",
    "Latitude",
    "Country",
    "Country_Code",
    "Hashtags",
]


def get_tweet_items(query):
    return sntwitter.TwitterSearchScraper(query).get_items()


def scrape_tweets(query, n=100):
    tweets_list = []
    tweets = get_tweet_items(query)
    for i, tweet in enumerate(tweets):
        if i > n:
            break
        else:
            tweets_list.append(
                [
                    tweet.id,
                    tweet.date,
                    tweet.sourceLabel,
                    tweet.content,
                    tweet.url,
                    tweet.user.id,
                    tweet.user.username,
                    tweet.user.followersCount,
                    tweet.replyCount,
                    tweet.retweetCount,
                    tweet.likeCount,
                    tweet.quoteCount,
                    tweet.lang,
                    getattr(tweet.coordinates, "longitude", None),
                    getattr(tweet.coordinates, "latitude", None),
                    getattr(tweet.place, "country", None),
                    getattr(tweet.place, "countryCode", None),
                    tweet.hashtags,
                ]
            )

    return tweets_list


def create_dataframe_from_tweets_list(tweets_list, save=False):
    df = pd.DataFrame(tweets_list, columns=HEADER)
    if save:
        df.to_csv("test_df.csv", index=False)
    return df


if __name__ == "__main__":
    tweets = scrape_tweets("azuki")
    df = create_dataframe_from_tweets_list(tweets, save=True)
