import random

from twython import Twython

from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET


def build_chain(text, chain={}):
    words = text.split(' ')
    index = 1
    for word in words[index:]:
        key = words[index - 1]
        if key in chain:
            chain[key].append(word)
        else:
            chain[key] = [word]
        index += 1
    return chain


def generate_message(chain, count=50):
    word1 = random.choice(list(chain.keys()))
    message = word1.capitalize()
    while len(message.split(' ')) < count:
        word2 = random.choice(chain[word1])
        word1 = word2
        message += ' ' + word2
    return message


def write_file(filename, message):
    with open(filename, 'w') as f:
        f.write(message)


def make_tweet(tweet):
    while len(tweet) > 139:
        words = tweet.split(' ')
        words.pop()
        tweet = ' '.join(words)
    if tweet[-1] != '.':
        tweet += '.'
    return tweet


def get_tweets(user, count=50):

    twitter = Twython(CONSUMER_KEY,
                      CONSUMER_SECRET,
                      ACCESS_TOKEN,
                      ACCESS_SECRET)

    user_timeline = twitter.get_user_timeline(screen_name=user,
                                              count=count,
                                              include_retweets=False)

    tweets = []
    for tweet in user_timeline:
        tweets.append(tweet)

    return tweets


def main():
    tweets = ' '.join(get_tweets('realDonaldTrump'))
    chain = build_chain(tweets)
    message = generate_message(chain)
    tweet = make_tweet(message)
    print(tweet)


if __name__ == '__main__':
    main()
