import pandas as pd
import snscrape.modules.twitter as sntwitter

def get_tweet_items(query):
    return sntwitter.TwitterSearchScraper(query).get_items()

def scrape_tweets(query):
    tweets_list = []
    tweets = get_tweet_items(query)
    for i, tweet in enumerate(tweets):
        if i > 5:
            break
        else:
            tweets_list.append([tweet.date, tweet.id, tweet.sourceLabel, tweet.content, tweet.url, tweet.user.id, \
                        tweet.user.username, tweet.user.followersCount, tweet.replyCount,\
                        tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.lang,\
                        tweet.outlinks, tweet.retweetedTweet, tweet.quotedTweet,\
                        tweet.inReplyToTweetId, tweet.inReplyToUser, tweet.mentionedUsers,\
                        tweet.coordinates, tweet.place, tweet.hashtags, tweet.cashtags])

    return tweets_list

def create_dataframe_from_tweets_list(tweets_list):
    return pd.DataFrame(tweets_list)

if __name__ == "__main__":
    tweets = scrape_tweets("sengoku degens")
    df = create_dataframe_from_tweets_list(tweets)