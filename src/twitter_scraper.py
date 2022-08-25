import snscrape.modules.twitter as sntwitter

query = "sengoku degens OR #sengokudegens"

tweets = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > 1000:
        break
    else:
        tweets.append([tweet.date, tweet.id, tweet.sourceLabel, tweet.content, tweet.url, tweet.user.id, \
                      tweet.user.username, tweet.user.followersCount, tweet.replyCount,\
                      tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.lang,\
                      tweet.outlinks, tweet.retweetedTweet, tweet.quotedTweet,\
                      tweet.inReplyToTweetId, tweet.inReplyToUser, tweet.mentionedUsers,\
                      tweet.coordinates, tweet.place, tweet.hashtags, tweet.cashtags])