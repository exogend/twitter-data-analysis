from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sqlite3

# connect to DB and create cursor
#	if DB doesn't exist it will create one with this filename
conn = sqlite3.connect('twitterDB.sqlite')
cur = conn.cursor()

# check if user table exists to determine if DB file is already setup
cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="user"')
table_exists = cur.fetchone()

if table_exists == None: # if none then create tables
	# create user table
	print 'Creating tables'
	cur.execute('''
		CREATE TABLE `user` (
			`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			`name`	TEXT,
			`followers`	INTEGER,
			`latitude`	NUMERIC,
			`longitude`	NUMERIC
		);
		''')

	# create tweet table
	cur.execute('''
		CREATE TABLE `tweet` (
			`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			`user_id`	INTEGER,
			`tweet_text`	TEXT,
			`time_created`	TEXT,
			`latitude`	NUMERIC,
			`longitude`	NUMERIC
		);
		''')
	conn.commit()

# will need to generate tokens from https://apps.twitter.com/ and copy paste them here
access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''

class Listener(StreamListener):
	def on_data(self, data):
		data = json.loads(data)
		try:
			print data['text']

			# user info
			screen_name = data['user']['screen_name']
			followers = data['user']['followers_count']
			
			cur.execute('SELECT * FROM user WHERE name = ?', (screen_name,))
			_x = cur.fetchone()
			
			if _x == None: # if user not already in table
				cur.execute('INSERT INTO user(name,followers) VALUES (?,?)', (screen_name,followers))
				conn.commit()
			
			#tweet info
			cur.execute('SELECT id FROM user WHERE name = ?', (screen_name,))
			user_id = cur.fetchone()[0]
			tweet = data['text']
			time_created = data['created_at']

			if data['coordinates'] == None:
				latitude = None
				longitude = None
			else:
				longitude = data['coordinates']['coordinates'][1]
				latitude = data['coordinates']['coordinates'][1]

			_y = (user_id, tweet, time_created, latitude, longitude)
			cur.execute('INSERT INTO tweet(user_id, tweet_text, time_created, latitude, longitude) VALUES (?,?,?,?,?)', _y)
			conn.commit()

			return True

		except KeyError:
			#
			print 'Error, wait and restart stream'
			return False
		
		
	def on_error(self, status):
		print 'Error: ' + str(status)
		return False


if __name__ == '__main__':
	print 'Stream beginning\n'
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	twitterStream = Stream(auth, Listener())
	# currently set to filter tweets containing word 'python'
	# many other options for filtering
	twitterStream.filter(track=['python'])
	# Note: some words like "Trump" for example will yield too many tweets for Streaming API to handle
	# Would have to use another method for these