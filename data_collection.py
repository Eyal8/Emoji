import tweepy
import csv
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import got

def tweepy_connect():
  '''
  connect to tweepy
  :return: api
  '''
  consumer_key = 'LDMubo3sWG2ZbYbSpJ4NC3FjQ'
  consumer_secret = 'PHW2S0adhVC5WGucbFT0mN7uCwZpTQJ4U90f0g5Cye0Zno0KwP'
  access_token = '1009518634027376640-htB1fcPQJlaLPfxYzT3wmyH6rSkn3W'
  access_token_secret = 'G0CWlbov0Oyhm7ZHs9JbOvxnIMzQe2QvToAfPkjJVg5S0'

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth,wait_on_rate_limit=True)
  return api

def get_emojies_unicodes(URL):
  s = requests.get(URL).content.decode('utf-8')
  html = s
  soup = BeautifulSoup(html, 'html.parser')
  unicodes = defaultdict(str)
  code_tds = list(soup.findAll('td', attrs={'class': 'code'}))
  code_tds = code_tds[::2]
  name_tds = soup.findAll('td', attrs={'class': 'name'})
  for unicode, name in zip(code_tds, name_tds):
    current_unicode = str(unicode.text).replace('\n', '')
    if 'U' in current_unicode:
      unicodes[current_unicode] = name.text
  return unicodes


def collect_recent_tweets_with_emojies(unicodes, api):
  '''
  Collect tweets up until 7 days from today
  :param unicodes: dictionary of {key:emoji unicode(str), value: emoji description(str)}
  :return:
  '''
  for unicode in unicodes.keys():
    # Open/create a file to append data to
    file_path = str('Data/' + unicode + '.csv')
    csvFile = open(file_path, 'w+')

    #Use csv writer
    csvWriter = csv.writer(csvFile)

    for tweet in tweepy.Cursor(api.search, q = unicode, tweet_mode='extended', lang='en').items():

        # Write a row to the CSV file. I use encode UTF-8
        csvWriter.writerow([tweet.created_at, tweet.full_text.encode('utf-8')])
    csvFile.close()


def printTweet(descr, t):
  print(descr)
  print("Username: %s" % t.username)
  print("Retweets: %d" % t.retweets)
  print("Text: %s" % t.text)
  print("Mentions: %s" % t.mentions)
  print("Hashtags: %s\n" % t.hashtags)



def collect_old_tweets_with_emojies(start_date, end_date, max_tweets):
  '''
  collect old tweets by specifying a date
  :param start_date: starting date to collect tweets from. format: "yyyy-mm-dd"
  :param end_date: end date to collect tweets. format: "yyyy-mm-dd"
  :param max_tweets: max tweets to collect in each request
  :return:
  '''
  # Example 1 - Get tweets by username
  tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
  tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

  printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)

  # Example 2 - Get tweets by query search
  tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees').setSince("2015-05-01").setUntil(
    "2015-09-30").setMaxTweets(1)
  tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

  printTweet("### Example 2 - Get tweets by query search [europe refugees]", tweet)

  # Example 3 - Get tweets by username and bound dates
  tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil(
    "2015-09-12").setMaxTweets(1)
  tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

  printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']", tweet)


if __name__ == '__main__':
  api = tweepy_connect()
  unicodes = get_emojies_unicodes(URL='https://apps.timwhitlock.info/emoji/tables/unicode')
# # write unicodes to a file
# with open('Json_Unicodes.txt', 'w') as file:
#   file.write(json.dumps(unicodes))
  collect_recent_tweets_with_emojies(unicodes, api)
  collect_old_tweets_with_emojies('2015-09-10', '2015-09-10', 100)
